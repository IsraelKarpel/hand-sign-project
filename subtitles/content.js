const script = document.createElement('script')
script.setAttribute('type', 'module');
script.setAttribute('src', 'https://unpkg.com/pose-viewer@0.2.3/dist/pose-viewer/pose-viewer.esm.js');
document.body.appendChild(script);


function execute(fn, attributes = []) {
  const script = document.createElement("script")
  script.innerHTML = '(' + fn.toString() + `)(${attributes.join(', ')})`
  document.head.appendChild(script)
}

async function captionYouTube() {
  execute(async function () {
    await customElements.whenDefined('pose-viewer');
    const PoseViewer = customElements.get('pose-viewer');
    const el = new PoseViewer();

     el.setAttribute('width', '100');
    el.setAttribute("style", "background-color: rgba(255,255,255,0.5)")


    const url = window.location.href;
    const rx = /^.*(?:(?:youtu\.be\/|v\/|vi\/|u\/\w\/|embed\/)|(?:(?:watch)?\?v(?:i)?=|\&v(?:i)?=))([^#\&\?]*).*/;
    const videoId = url.match(rx)[1];

    el.setAttribute("src", 'https://nlp.biu.ac.il/~ccohenya8/sign/youtube/?v=' + videoId + '&lang=en.us');

    const [video] = document.getElementsByTagName("video");
    el.syncMedia(video);
    video.parentElement.parentElement.getElementsByClassName("ytp-paid-content-overlay")[0].appendChild(el);
  });
}


function captionHTML5() {
  execute(function () {
    const videos = document.querySelectorAll("video");
    for (const video of videos) {
      let trackId = 0;

      video.addEventListener("play", async () => {
        const track = Array.from(video.children).filter(e => e.nodeName === "TRACK")[trackId];

        await customElements.whenDefined('pose-viewer');
        const poseViewer = customElements.get('pose-viewer');
        poseViewer.setAttribute("width", "50%");
        poseViewer.setAttribute("src", `https://nlp.biu.ac.il/~ccohenya8/sign/video/?path=${encodeURIComponent(track.src)}&lang=${"en.us"}`);


        poseViewer.addEventListener("firstRender$", () => {
          const canvas = poseViewer.shadowRoot.querySelector("canvas");
          const width = Number(canvas.getAttribute("width"));
          const videoWidth = video.videoWidth;
          poseViewer.style.left = "80%"
          poseViewer.style.bottom = "20%"
          poseViewer.style.zoom = (videoWidth / 10) / width;
        });

        video.parentElement.appendChild(poseViewer);
        poseViewer.syncMedia(video);
      });
    }
  });
}

chrome.runtime.onMessage.addListener(async () => {
  const url = window.location.host

  if (url.includes("youtube")) {
    return captionYouTube();
  } else {
    return captionHTML5();
  }
})



