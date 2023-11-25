;(() => {

let cam_device, cam_devices
let cam_device_labels = {}

let camera, camSwapBtn, camCanvas, photo, photoBtn, backBtn, submitBtn, acctDiv, noteDiv, noteTxt, acctPhoto, acctName
const elesById = () => {
    camera = document.getElementById('camera')
    camSwapBtn = document.getElementById('swap-camera-btn')
    camCanvas = document.getElementById('cam-canvas')
    photo = document.getElementById('photo')
    photoBtn = document.getElementById('take-photo')
    backBtn = document.getElementById('back-btn')
    submitBtn = document.getElementById('submit')
    acctDiv = document.getElementById('account-div')
    noteDiv = document.getElementById('notebook-div')
    noteTxt = document.getElementById('notebook')
    acctPhoto = document.getElementById('acct-photo')
    acctName = document.getElementById('acct-name')
}

const findCameras = () => {
    navigator.mediaDevices.enumerateDevices().then((devices) => {
        const video_devices = devices.filter(device => device.kind === 'videoinput')
        cam_devices = video_devices.map(d => d.deviceId)
        for (const d of video_devices) {
            cam_device_labels[d.deviceId] = d.label
        }
    })
    .catch(err => console.error(`Couldn't get camera devices: ${err}`))
}

const startCamera = () => {
    camera.pause()
    camSwapBtn.innerHTML = `🔄️ ...`
    camera.classList.add('cam-swapping')

    navigator.mediaDevices
        .getUserMedia({
            video: {
                aspectRatio: 1,
                facingMode: cam_device ? undefined : 'user',
                deviceId: cam_device,
            },
            audio: false,
        })
        .then(stream => {
            cam_device = cam_device ?? stream.getVideoTracks()[0].getSettings().deviceId
            camSwapBtn.innerHTML = `🔄️ ${cam_device_labels[cam_device]}`
            camera.srcObject = stream
            camera.classList.remove('cam-swapping')
            camera.play()
        })
        .catch(err => {
            console.error(`Couldn't get camera stream: ${err}`)
            camera.play()
            camSwapBtn.innerHTML = `🔄️ ${cam_device_labels[cam_device]}`
            camera.classList.remove('cam-swapping')
        })
}

const setupSwapCamera = () => {
    camSwapBtn.onclick = () => {
        cam_device = cam_devices[(cam_devices.indexOf(cam_device) + 1) % cam_devices.length]
        startCamera()
    }
}

const takePhoto = () => {
    const maxDim = Math.max(camera.videoHeight, camera.videoWidth)
    const extraWid = (maxDim - camera.videoHeight)
    const extraHgt = (maxDim - camera.videoWidth)

    // draw cropped square from video, 350 x 350
    camCanvas.getContext('2d').drawImage(
        camera,
        extraWid / 2, extraHgt / 2,
        camera.videoWidth - extraWid, camera.videoHeight - extraHgt,
        0,0,
        camCanvas.width,
        camCanvas.height
    )
    const data = camCanvas.toDataURL('image/png')
    photo.src = data
    acctPhoto.src = data
}

let loginAbort = new AbortController();

const confirmPhoto = () => {
    submitBtn.onclick = () => {
        submitBtn.disabled = true
        submitBtn.textContent = '...'
        const dotdotdot = setInterval(() => {
            submitBtn.textContent = '.'.repeat(submitBtn.textContent.length % 3 + 1)
        }, 500)

        fetch('/login', {
            method: "POST",
            body: photo.src,
            signal: loginAbort.signal,
        })
        .then(async res => {
            clearInterval(dotdotdot)
            r = await res.json()
            switch (r.status) {
            case 'ok':
                camera.srcObject = null
                acctName.textContent = r.username
                acctDiv.classList.remove('grow')
                acctDiv.classList.add('shrink')
                noteDiv.classList.remove('shrink')
                noteDiv.classList.add('grow')
                noteTxt.value = r.content
                break
            default:
                console.warn(`Unknown login response status: ${r.status}`);
            }
        })
        .catch(err => {
            clearInterval(dotdotdot)
            submitBtn.textContent = 'Continue'
            submitBtn.disabled = false
            if (loginAbort.signal.aborted) {
                console.log('Login cancelled.');
                loginAbort = new AbortController();
            }
            else {
                submitBtn.classList.add('error')
                console.error(`Error logging in: ${err}`)
            }
        })
    }
}

const setupPhoto = () => {
    photoBtn.onclick = () => {
        takePhoto()
        photo.classList.add('flash')
        photo.style.display = 'block'
        photoBtn.style.display = 'none'
        backBtn.style.display = 'block'
        submitBtn.style.display = 'block'
    }
    backBtn.onclick = () => {
        if (submitBtn.disabled) loginAbort.abort()
        photo.style.display = 'none'
        photo.classList.remove('flash')
        photoBtn.style.display = 'block'
        backBtn.style.display = 'none'
        submitBtn.style.display = 'none'
        submitBtn.classList.remove('error')
    }
    confirmPhoto()
}

const init = () => {
    elesById()
    findCameras()
    startCamera()
    setupSwapCamera()
    setupPhoto()
}

if (document.readyState !== "loading") init()
else window.addEventListener("load", init)

})();