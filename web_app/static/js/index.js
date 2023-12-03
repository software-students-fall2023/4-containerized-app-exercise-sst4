(() => {
	let cam_device, cam_devices;
	let cam_device_labels = {};

	let camera,
		camSwapBtn,
		camCanvas,
		photo,
		photoBtn,
		backBtn,
		submitBtn,
		registerBtn,
		registrationForm,
		registerConfirmBtn,
		acctDiv,
		noteDiv,
		noteTxt,
		acctPhoto,
		acctName,
		messageContainer;
	const elesById = () => {
		camera = document.getElementById("camera");
		camSwapBtn = document.getElementById("swap-camera-btn");
		camCanvas = document.getElementById("cam-canvas");
		photo = document.getElementById("photo");
		photoBtn = document.getElementById("take-photo");
		backBtn = document.getElementById("back-btn");
		submitBtn = document.getElementById("submit");
		registerBtn = document.getElementById("register");
		registrationForm = document.getElementById("registration-form");
		registerConfirmBtn = document.getElementById("register-confirm");
		acctDiv = document.getElementById("account-div");
		noteDiv = document.getElementById("notebook-div");
		noteTxt = document.getElementById("notebook");
		acctPhoto = document.getElementById("acct-photo");
		acctName = document.getElementById("acct-name");
		messageContainer = document.getElementById("message-container");
	};

	const findCameras = () => {
		navigator.mediaDevices
			.enumerateDevices()
			.then((devices) => {
				const video_devices = devices.filter((device) => device.kind === "videoinput");
				cam_devices = video_devices.map((d) => d.deviceId);
				for (const d of video_devices) {
					cam_device_labels[d.deviceId] = d.label;
				}
			})
			.catch((err) => console.error(`Couldn't get camera devices: ${err}`));
	};

	const startCamera = () => {
		camera.pause();
		camSwapBtn.innerHTML = `🔄️ ...`;
		camera.classList.add("cam-swapping");

		navigator.mediaDevices
			.getUserMedia({
				video: {
					aspectRatio: 1,
					facingMode: cam_device ? undefined : "user",
					deviceId: cam_device,
				},
				audio: false,
			})
			.then((stream) => {
				cam_device = cam_device ?? stream.getVideoTracks()[0].getSettings().deviceId;
				camSwapBtn.innerHTML = `🔄️ ${cam_device_labels[cam_device]}`;
				camera.srcObject = stream;
				camera.classList.remove("cam-swapping");
				camera.play();
			})
			.catch((err) => {
				console.error(`Couldn't get camera stream: ${err}`);
				camera.play();
				camSwapBtn.innerHTML = `🔄️ ${cam_device_labels[cam_device]}`;
				camera.classList.remove("cam-swapping");
			});
	};

	const setupSwapCamera = () => {
		camSwapBtn.onclick = () => {
			cam_device = cam_devices[(cam_devices.indexOf(cam_device) + 1) % cam_devices.length];
			startCamera();
		};
	};

	const takePhoto = () => {
		const maxDim = Math.max(camera.videoHeight, camera.videoWidth);
		const extraWid = maxDim - camera.videoHeight;
		const extraHgt = maxDim - camera.videoWidth;

		// draw cropped square from video, 350 x 350
		camCanvas
			.getContext("2d")
			.drawImage(
				camera,
				extraWid / 2,
				extraHgt / 2,
				camera.videoWidth - extraWid,
				camera.videoHeight - extraHgt,
				0,
				0,
				camCanvas.width,
				camCanvas.height
			);
		const data = camCanvas.toDataURL("image/jpeg"); //png?
		photo.src = data;
		acctPhoto.src = data;
	};

	let loginAbort = new AbortController();

	const confirmPhoto = () => {
		submitBtn.onclick = () => {
			submitBtn.disabled = true;
			submitBtn.textContent = "...";

			sendImageData(photo.src);
		};
	};

	const registerButton = () => {
		registerBtn.onclick = () => {
			messageContainer.style.display = "none";

			registerBtn.style.display = "none";
			registerConfirmBtn.style.display = "block";
			registerConfirmBtn.disabled = true;
			registrationForm.elements["name"].value = "";
			registrationForm.style.display = "block";
		};
		registrationForm.onkeyup = () => {
			if (registrationForm.elements["name"].value == "") {
				registerConfirmBtn.disabled = true;
			} else {
				registerConfirmBtn.disabled = false;
			}
		};
		registerConfirmBtn.onclick = () => {
			registerConfirmBtn.textContent = "...";

			const dotdotdot = setInterval(() => {
				registerConfirmBtn.textContent = ".".repeat((submitBtn.textContent.length % 3) + 1);
			}, 500);

			userName = registrationForm.elements["name"].value;
			fetch("/register", {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify({ name: userName, image: photo.src }),
			})
				.then((response) => response.json())
				.then((data) => {
					clearInterval(dotdotdot);
					registerConfirmBtn.disabled = true;
					registrationForm.style.display = "none";
					registerConfirmBtn.textContent = "Added!";
				})
				.catch((error) => {
					console.error("Error sending image data to the backend:", error);
					clearInterval(dotdotdot);
					registerConfirmBtn.disabled = true;
					registrationForm.style.display = "none";
					registerConfirmBtn.textContent = "Something went wrong.";
				});
		};
	};

	const setupPhoto = () => {
		photoBtn.onclick = () => {
			takePhoto();
			photo.classList.add("flash");
			photo.style.display = "block";
			photoBtn.style.display = "none";
			backBtn.style.display = "block";
			submitBtn.style.display = "block";
		};
		backBtn.onclick = () => {
			if (submitBtn.disabled) loginAbort.abort();
			photo.style.display = "none";
			photo.classList.remove("flash");
			photoBtn.style.display = "block";
			backBtn.style.display = "none";
			submitBtn.style.display = "none";
			submitBtn.classList.remove("error");
			submitBtn.textContent = "Continue";
			submitBtn.disabled = false;
			registerBtn.style.display = "none";
			registerConfirmBtn.style.display = "none";
			registrationForm.style.display = "none";
			messageContainer.style.display = "block";
			messageContainer.textContent = "Result of your photo analysis will appear here.";
		};
		confirmPhoto();
		registerButton();
	};

	const init = () => {
		elesById();
		findCameras();
		startCamera();
		setupSwapCamera();
		setupPhoto();
	};

	function sendImageData(imageData) {
		const dotdotdot = setInterval(() => {
			submitBtn.textContent = ".".repeat((submitBtn.textContent.length % 3) + 1);
		}, 500);

		fetch("recognize", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({ image: imageData }),
		})
			.then((response) => response.json())
			.then((data) => {
				console.log("Response from backend:", data);

				const message = data.message;
				messageContainer.textContent = message;

				clearInterval(dotdotdot);
				submitBtn.style.display = "none";

				if (message == "Face Not Recognized") {
					registerBtn.style.display = "block";
					registerBtn.textContent = "Register?";
					registerBtn.disabled = false;
				} else if (message == "No faces found in the captured image.") {
					registerBtn.style.display = "block";
					registerBtn.textContent = "No faces :(";
					registerBtn.disabled = true;
				} else {
					// Face Recognized
					registerBtn.style.display = "block";
					registerBtn.textContent = "Welcome Back!";
					registerBtn.disabled = true;
				}
			})
			.catch((error) => {
				console.error("Error sending image data to the backend:", error);
			});
	}

	if (document.readyState !== "loading") init();
	else window.addEventListener("load", init);
})();
