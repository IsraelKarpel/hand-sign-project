const serverUrl = 'http://localhost:4002'

const sendWordToServer = (word) => {
    
    // lower the words
    wordLower = word.value.toLowerCase();
    console.log(wordLower);

    fetch(`http://localhost:4002/wordFromClient?word=${wordLower}`).then(response => {
        // conver body -> json    
        return response.json() 
    })  .then(body => {
            if(wordLower == ''){
                alert('Enter a word please');
                return;
            }
            if(body.length === 0){
                console.log(body);
                alert('No videos found with that word, refresh the page and try another word:)');
                return;
            }
            const table = document.getElementById('video-table')
            console.log('body', body);
            console.log(wordLower);
            body.slice(0,5).forEach((item) => {
                
                // find start and end from sentences
                let sentenceToShow;
                let lengthOfSentences = item.sentences.length;
                console.log(lengthOfSentences);
                for(i=0 ; i< lengthOfSentences ; i++){
                    sentenceToShow = item.sentences[i].text;
                    // find the sentence into the text 
                    if(sentenceToShow.indexOf(wordLower) >= 0){
                        
                        startTimeVideo = item.sentences[i].start;
                        endTimeVideo = item.sentences[i].end;
                         console.log(sentenceToShow);
                         console.log(startTimeVideo);
                        console.log(endTimeVideo);
                        console.log(wordLower);
                table.innerHTML += `
                <tr class="style1">
                    <td>${sentenceToShow}</td>
                    <td id="changable">
                    <pose-viewer width='200px' src="${serverUrl}/static/${item.hashUrl}.pose" start=${item.startTimeVideo} end=${item.endTimeVideo} loop autoplay ></pose-format> 
                        <script src="https://unpkg.com/pose-viewer@0.1.5/dist/pose-viewer/pose-viewer.esm.js" type="module"></script>
                    </td>
                </tr> 
            `;
             }
            }
        })
    })
}


