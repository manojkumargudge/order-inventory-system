pipeline {
    agent any

    environment {
        AWS_REGION  = 'ap-south-1'

        ECR_REPO    = 'order-inventory-system'
        ECS_CLUSTER = 'order-inventory-cluster'
        ECS_SERVICE = 'order-inventory-service'
        TASK_FAMILY = 'order-inventory-task'

        IMAGE_TAG = "${env.GIT_COMMIT}"
    }

    options {
        timestamps()
        disableConcurrentBuilds()
        buildDiscarder(
            logRotator(numToKeepStr: '20')
        )
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Lint (ruff)') {
            when {
                branch 'main'
            }

            agent {
                docker {
                    image 'python:3.14-slim'
                    reuseNode true
                }
            }

            steps {
                sh '''
                    pip install --no-cache-dir ruff
                    ruff check src/
                '''
            }
        }

        stage('Type Check (mypy)') {
            when {
                branch 'main'
            }

            agent {
                docker {
                    image 'python:3.14-slim'
                    reuseNode true
                }
            }

            steps {
                sh '''
                    pip install --no-cache-dir \
                        -r requirements.txt \
                        mypy \
                        types-python-jose

                    mypy src/
                '''
            }
        }

        stage('Test (pytest)') {
            when {
                branch 'main'
            }

            steps {
                script {
                    sh '''
                        docker network create ci-test-net || true

                        docker run -d --rm \
                            --name ci-postgres \
                            --network ci-test-net \
                            -e POSTGRES_USER=test \
                            -e POSTGRES_PASSWORD=test \
                            -e POSTGRES_DB=test_db \
                            postgres:16-alpine

                        sleep 5
                    '''

                    try {
                        sh '''
                            docker run --rm \
                                --network ci-test-net \
                                -v "$PWD":/app \
                                -w /app \
                                -e DATABASE_URL=postgresql+asyncpg://test:test@ci-postgres:5432/test_db \
                                -e APP_NAME=order-inventory-system \
                                -e APP_VERSION=0.1.0 \
                                -e ENVIRONMENT=test \
                                -e DEBUG=False \
                                -e SECRET_KEY=ci-test-secret \
                                -e ALGORITHM=HS256 \
                                -e ACCESS_TOKEN_EXPIRE_MINUTES=30 \
                                python:3.14-slim \
                                sh -c "
                                    pip install --no-cache-dir \
                                        -r requirements.txt \
                                        types-python-jose &&
                                    pytest --junitxml=report.xml
                                "
                        '''
                    } finally {
                        sh 'docker stop ci-postgres || true'
                        sh 'docker network rm ci-test-net || true'
                    }
                }
            }

            post {
                always {
                    junit(
                        allowEmptyResults: true,
                        testResults: 'report.xml'
                    )
                }
            }
        }

        stage('Build Docker Image') {
            when {
                branch 'main'
            }

            steps {
                sh '''
                    docker build \
                        -t ${ECR_REPO}:${IMAGE_TAG} \
                        .
                '''
            }
        }

        stage('Push to ECR') {
            when {
                branch 'main'
            }

            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'aws-credentials',
                        usernameVariable: 'AWS_ACCESS_KEY_ID',
                        passwordVariable: 'AWS_SECRET_ACCESS_KEY'
                    )
                ]) {
                    sh '''
                        set -e

                        AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
                        ECR_URI="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO}"

                        echo "Logging in to ECR..."

                        aws ecr get-login-password \
                            --region ${AWS_REGION} | \
                            docker login \
                            --username AWS \
                            --password-stdin ${ECR_URI}

                        echo "Tagging Docker image..."

                        docker tag \
                            ${ECR_REPO}:${IMAGE_TAG} \
                            ${ECR_URI}:${IMAGE_TAG}

                        echo "Pushing Docker image..."

                        docker push \
                            ${ECR_URI}:${IMAGE_TAG}

                        echo "ECR push completed successfully."
                    '''
                }
            }
        }

        stage('Deploy to ECS') {
            when {
                branch 'main'
            }

            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'aws-credentials',
                        usernameVariable: 'AWS_ACCESS_KEY_ID',
                        passwordVariable: 'AWS_SECRET_ACCESS_KEY'
                    )
                ]) {
                    sh '''
                        set -e

                        AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
                        ECR_URI="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO}"

                        echo "Getting current ECS task definition..."

                        aws ecs describe-task-definition \
                            --task-definition ${TASK_FAMILY} \
                            --region ${AWS_REGION} \
                            --query 'taskDefinition' \
                            > current-task-def.json

                        echo "Rendering new task definition..."

                        python3 \
                            ecs/render_task_def.py \
                            current-task-def.json \
                            "${ECR_URI}:${IMAGE_TAG}" \
                            new-task-def.json

                        echo "Registering new ECS task definition..."

                        NEW_TASK_ARN=$(aws ecs register-task-definition \
                            --region ${AWS_REGION} \
                            --cli-input-json file://new-task-def.json \
                            --query 'taskDefinition.taskDefinitionArn' \
                            --output text)

                        echo "New task definition:"
                        echo "$NEW_TASK_ARN"

                        echo "Updating ECS service..."

                        aws ecs update-service \
                            --cluster ${ECS_CLUSTER} \
                            --service ${ECS_SERVICE} \
                            --task-definition "$NEW_TASK_ARN" \
                            --region ${AWS_REGION}

                        echo "Waiting for ECS service to become stable..."

                        aws ecs wait services-stable \
                            --cluster ${ECS_CLUSTER} \
                            --services ${ECS_SERVICE} \
                            --region ${AWS_REGION}

                        echo "ECS deployment completed successfully."
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "Build ${IMAGE_TAG} succeeded."
        }

        failure {
            echo "Build failed. Check the stage logs above."
        }

        always {
            sh '''
                docker image prune -f || true
            '''
        }
    }
}