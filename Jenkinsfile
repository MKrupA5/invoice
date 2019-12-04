
properties([
	parameters([
        string(defaultValue: "master", description: 'Which Git Branch to clone?', name: 'GIT_BRANCH'),
	])
])

try {

  stage('Checkout'){
    node('master'){
        checkout([$class: 'GitSCM', branches: [[name: '*/$GIT_BRANCH']], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], userRemoteConfigs: [[url: 'https://github.com/wparth/invoice.git']]])
    }
  }
  }

  stage('Build And Push Docker Image') {
    node('master'){
      sh "$(aws ecr get-login --no-include-email --region ap-south-1)"
      sh "docker build -t 703569030910.dkr.ecr.ap-south-1.amazonaws.com/invoice:${BUILD_NUMBER} ."
      sh "docker push 703569030910.dkr.ecr.ap-south-1.amazonaws.com/invoice:${BUILD_NUMBER}"
    }
  }

  stage('Container Security Scan') {
  	node('master'){
  	    sh 'echo "703569030910.dkr.ecr.ap-south-1.amazonaws.com/invoice:${BUILD_NUMBER} `pwd`/Dockerfile" > anchore_images'
  	    anchore autoSubscribeTagUpdates: false, bailOnFail: false, bailOnPluginFail: false, name: 'anchore_images'
      	}
    }
    
  stage('Cleanup') {
      node('master') {
          sh ''' for i in `cat anchore_images | awk '{print $1}'`;do docker rmi $i; done '''
      }   
    }

  stage('Deploy on Dev') {
  	node('master'){
        sh ''' sed -i 's/VERSION/'"${BUILD_NUMBER}"'/g' deployment.yaml '''
  	    sh "kubectl apply -f deployment.yaml"
      	}
    }
}
catch (err){
    currentBuild.result = "FAILURE"
    throw err
}
