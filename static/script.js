async function uploadPDF(event){
    const btn=event.target,files=document.getElementById("pdf").files;
    if(!files.length) return alert("Choose at least one PDF.");

    btn.disabled=true;
    btn.innerHTML="Uploading...";
    document.getElementById("answer").innerHTML=`Uploading PDFs...

Reading documents...

Extracting text...

Building knowledge base...

Please wait...`;

    const formData=new FormData();
    [...files].forEach(f=>formData.append("files",f));

    try{
        const res=await fetch("/upload",{method:"POST",body:formData});
        document.getElementById("answer").innerHTML=(await res.json()).message.join("<br>");
    }catch{
        document.getElementById("answer").innerHTML="Upload failed.";
    }

    btn.disabled=false;
    btn.innerHTML="UPLOAD";
}

async function askQuestion(event){
    const btn=event.target,
          question=document.getElementById("question").value.trim();

    if(!question) return alert("Enter a question.");

    btn.disabled=true;
    btn.innerHTML="Thinking...";

    document.getElementById("answer").innerHTML=`Searching knowledge base...

Retrieving relevant information...

Generating answer...`;

    const formData=new FormData();
    formData.append("question",question);
    formData.append("model",document.getElementById("model").value);

    try{
        const res=await fetch("/ask",{method:"POST",body:formData});
        const data=await res.json();
        document.getElementById("answer").innerHTML=data.answer;
        document.getElementById("source").innerHTML="<b>Sources</b><br><br>• "+data.source.join("<br>• ");
    }catch{
        document.getElementById("answer").innerHTML="Unable to get a response.";
    }

    btn.disabled=false;
    btn.innerHTML="EXECUTE";
}
