# FacialBook

![webapp workflow](https://github.com/software-students-fall2023/4-containerized-app-exercise-sst4/actions/workflows/web-app.yml/badge.svg)
![mlc workflow](https://github.com/software-students-fall2023/4-containerized-app-exercise-sst4/actions/workflows/machine-learning-client.yml/badge.svg)

## What is FacialBook?

We have created a face recognition web application that takes a picture of you and if it recognizes you it will greet you by name. If it does not recognize you, you will be given the opportunity to register yourself to the database. After taking a photo and if it does not recognize you, you will be prompted to type your name which it will save along with the photo you took. You may then go back and capture your face once again and the app should recognize who you are.

## How To Run

### From Digital Ocean Deployment

If you want to run deployed version go to: [http://137.184.181.41:5000/](http://137.184.181.41:5000/). You may have to allow the browser to recognize the website as secure in order to run the camera.

#### Using Mozilla Firefox

1. In a new tab, type in `about:config`.
2. Set `media.devices.insecure.enabled` and `media.getusermedia.insecure.enabled` to `true`.
3. Reload [http://137.184.181.41:5000/](http://137.184.181.41:5000/).
4. On prompt, allow the site to access your camera.

#### Using Chrome

1. Open a new tab and copy paste the following link into the address: `chrome://settings/content/insecureContent`.
2. Under "Allowed to show insecure content" click "Add".
3. Add [http://137.184.181.41:5000/](http://137.184.181.41:5000/) as the site URL.
4. Go back to the page and reload, on prompt, allow the site to access your camera.

### Locally with Docker

Please make sure that Docker Desktop is installed and running.
Please go into the root directory and type `docker-compose up --build`.
Please wait for the build to complete, please be aware that due to the large amount of libraries that need to be installed for the Machine Learning Client this can take up to potentially 10-15 minutes.
Please go to [http://127.0.0.1:5000](http://127.0.0.1:5000) to use the app.
Please make sure that the browser you use has the ability to have access to your camera and please be sure to turn your camera on, this works best with a built in laptop camera. If you are using a USB webcam, you may need to reload the page before the application registers camera input.

## Contributors

[Richard Li](https://github.com/Silver1793) \
[Ryan Zhang](https://github.com/CouriersRyan) \
[Allyson Chan](https://github.com/tinybitofheaven) \
[Brad Feng](https://github.com/BradFeng02)
