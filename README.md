![example workflow](https://github.com/software-students-fall2023/4-containerized-app-exercise-sst4/actions/workflows/python-package.yml/badge.svg)

### What is our app?

We have created a face recognizing web app. The app take a picture of you and if it recognizes you it will print your name to the screen. If it does not recognize you, you will be given the opportunity to register yourself. You will be prompted to type your name and then take another picture of yourself which will be uploaded to the database. You may then go back and capture your face once again and the app should recognize who you are.

### How To Run

Please make sure that docker desktop is installed and running.
Please go into the root directory and type `docker-compose --build`.
Please wait for the build to complete, please be aware that due to the large amount of libraries that need to be installed from the machine learning client this can take up to potentially 15 minutes.
Please go to your local host 5000 and use the app.
Please make sure that the browser you use has the ability to have access to your camera and please be sure to turn your camera on, this works best with a built in laptop camera.

### Contributors

[Richard Li](https://github.com/Silver1793)
[Ryan Zhang](https://github.com/CouriersRyan)
[Allyson Chan](https://github.com/tinybitofheaven)
[Brad Feng](https://github.com/BradFeng02)
