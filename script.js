//example POST method implementation: 
async function postData(url ="", data={}) {
    const response = await fetch(url,{
        method: "POST", headers: {
            "Content-Type": "application/json",
        },body: JSON.stringify(data),
    }) 
    return response.json();
}

function handleKeyPress(event) {
    // Check if Enter key (key code 13) is pressed
    if (event.key === 'Enter') {
        event.preventDefault(); // Prevent the form submission (if inside a form)

        // Trigger the button click
        const sendButton = document.getElementById('sendButton');
        sendButton.click();
    }
}
sendButton.addEventListener("click", async()=>{
    questionInput = document.getElementById("questionInput").value;
    document.getElementById("questionInput").value = "";
    document.querySelector(".right2").style.display ="block"
    document.querySelector(".right1").style.display ="none"

    question2.innerHTML = questionInput;
    question1.innerHTML = questionInput;
    //get the answer and populate it!
    let result = await postData("/api", {"question": questionInput});
    console.log("API Response:", result);
    //{"result": "droupadi murmur"}
    //solution.innerHTML = result.result;     
    //solution.innerHTML = result.answer;
    solution.innerHTML = `<pre>${result.answer}</pre>`;


})