let cam_device = undefined
let cam_devices = undefined
let cam_device_labels = {}

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
    const camera = document.getElementById('camera')
    const btn = document.getElementById('swap-camera-btn')

    camera.pause()
    btn.innerHTML = `🔄️ ...`
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
            btn.innerHTML = `🔄️ ${cam_device_labels[cam_device]}`
            camera.srcObject = stream
            camera.classList.remove('cam-swapping')
            camera.play()
        })
        .catch(err => {
            console.error(`Couldn't get camera stream: ${err}`)
            camera.play()
            btn.innerHTML = `🔄️ ${cam_device_labels[cam_device]}`
            camera.classList.remove('cam-swapping')

        })
}

const setupSwapCamera = () => {
    const btn = document.getElementById('swap-camera-btn')
    btn.onclick = () => {
        cam_device = cam_devices[(cam_devices.indexOf(cam_device) + 1) % cam_devices.length]
        startCamera()
    }
}

const testfunc = () => {
    const btn = document.getElementById('testbtn')
    btn.onclick = () => {
        const a = document.getElementById('account-div')
        const b = document.getElementById('notebook-div')
        if (a.classList.contains('shrink')) {
            a.classList.remove('shrink')
            b.classList.add('shrink')
            a.classList.add('grow')
            b.classList.remove('grow')
        } else {
            a.classList.add('shrink')
            b.classList.remove('shrink')
            a.classList.remove('grow')
            b.classList.add('grow')
        }
    }
}

const init = () => {
    findCameras()
    startCamera()
    setupSwapCamera()
}

if (document.readyState !== "loading") init()
else window.addEventListener("load", init)