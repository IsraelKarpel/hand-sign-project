
function createSentenses(str) {
    console.log(str);

    let result = []
    let timeRegex = /[0-9]{2}:[0-9]{2}\.[0-9]{3} --> [0-9]{2}:[0-9]{2}\.[0-9]{3}/
    let arr = str.split('\n').filter((str, i) => str !== '' && i !== 0)
  //  console.log(arr);
    arr.forEach(row => {
        if (timeRegex.exec(row)) {
            const [start, end] = row.split(' --> ')
            return result.push({ start: start, end: end, text: '' })
        }
        else result[result.length - 1].text += ` ${row}`
    })
    console.log('result', result.length);
    return result;
}



module.exports = {
    createSentenses,
  };