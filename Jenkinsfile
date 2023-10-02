pipeline {
  agent any
  stages {
    stage('Step 1') {
      steps {
        sh 'ls -a'
      }
    }

    stage('Step2') {
      steps {
        discordSend(webhookURL: 'https://discord.com/api/webhooks/1158210275141488701/9_61XBzxBKxrEQrwBeV_64r43YJ9qjrS524uhYRGcNeGzw8RTBPrMR6MvJpjm50Kiho_', customUsername: 'Test', description: 'Test', dynamicFieldContainer: 'test', thumbnail: 'test')
      }
    }

  }
}