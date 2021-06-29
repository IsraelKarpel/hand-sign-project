
//async function run() {
//    const res = await fetch('https://video.google.com/timedtext?lang=en&v=5MgBikgcWnY');
//    const body = await res.text();
//    console.log(Array.from(body.matchAll(/<text start="(\d*\.?\d*)" dur="(\d*\.?\d*)">([\s\S]*?)<\/text>/g)).map(m => ({start: m[1], end: m[2], text: m[3]})))
//}
//run()

chrome.runtime.onMessage.addListener(function (request) {

    const style = document.createElement("style")

    style.innerHTML = `
pose-viewer {
    position: absolute;
    z-index: 1;
    left: 0;
    bottom: 0;
    background: rgb(255 255 255 / 70%);
    border-radius: 50%;
}
`
    document.head.appendChild(style)
    console.log("d");
    url = window.location.host
    console.log(url)
    if (url.includes("youtube")) {

        video = document.getElementsByTagName("video")
        var id = Math.floor(Math.random() * 100).toString()
        video[0].setAttribute("id", id) 
        //local server that send image
        const sample_image = `<img width="30%" height=20%" data-layer="8" src='http://localhost:3000/'>`;
        video[0].parentElement.parentElement.getElementsByClassName("ytp-paid-content-overlay")[0].innerHTML += sample_image

    } else {
    videos = document.querySelectorAll("video")
    console.log(videos)
    //video = videos[0]
    videos.forEach(video => {
        let trackId = null;
       // for (let i = 0; i < video.textTracks.length; i++) {
         //   if (video.textTracks[i].mode === "showing") {
                //console.log(video.textTracks[i]);
                //trackId = video.textTracks[i];
           //     trackId = i;
           // }
        //}
        trackId = 0
        video.addEventListener("play", async () => {
            //console.log("noe play")
            var id = Math.floor(Math.random() * 100).toString()
            video.setAttribute("id", id)
            video.parentElement.style.position = 'relative';
            // this is the first time the video is playing. add the pose viewer thing if needed     
            // Get the track remote src
            const track = Array.from(video.children).filter(e => e.nodeName === "TRACK")[trackId];
            const subtitleSrc = track.src;
            console.log(subtitleSrc)
            // Add pose to page
       //     const poseViewer = `<pose-viewer src='https://nlp.biu.ac.il/~ccohenya8/sign/video/?path=${encodeURIComponent(
       //   subtitleSrc
       // )}&lang=${"en.us"}'></pose-viewer>`
        const poseViewer = `<pose-viewer src='http://localhost:3000'></pose-viewer>`;
            video.parentElement.innerHTML += poseViewer;
            const inject = `
                (async () => {
                    console.log("injected");
                    await customElements.whenDefined('pose-viewer');
                
                    const poseViewer = document.querySelector('pose-viewer');
                    const video = document.getElementById(${id});
                
                    poseViewer.syncMedia(video);
                })();`
            const script2 = document.createElement("script")
            script2.innerText = inject
            document.head.appendChild(script2)
            const poseViewerEl = document.querySelector("pose-viewer");
            console.log(poseViewerEl)

            const setWidth = () => {
                
                const svg = poseViewerEl.shadowRoot.querySelector("svg");
                const width = Number(svg.getAttribute("width"));
                //const videoWidth = video.getBoundingClientRect().width;
                var videoWidth = video.videoWidth;
                poseViewerEl.style.left = "80%"
                poseViewerEl.style.bottom = "20%" //"20%"
                poseViewerEl.style.zoom = (videoWidth / 10) / width;
            };
            setTimeout(setWidth, 1000); // TODO, this is bullshit, need event
            // When video changes size
             new ResizeObserver(setWidth).observe(video)
        });

    });
}
})



