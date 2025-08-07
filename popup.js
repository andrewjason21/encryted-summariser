const inputText = document.getElementById("inputText");
const resultDiv = document.getElementById("result");

// Load selected text from storage if any
chrome.storage.local.get('selectedText', data => {
  if (data.selectedText) inputText.value = data.selectedText;
});

document.getElementById("summarizeBtn").onclick = async () => {
  const text = inputText.value.trim();
  if (!text) {
    resultDiv.innerText = "Please paste or select some text.";
    return;
  }
  resultDiv.innerText = "Summarizing...";

  try {
    // Replace YOUR_GRADIO_PUBLIC_URL with your live Gradio app URL
    const response = await fetch("https://shauryanarang-text_summary_by_shaurya.hf.space/run/predict", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    data: [text, 3, 5, "english"]  // yahan parameters match hone chahiye backend ke hisaab se
  }),
});
const json = await response.json();

    // json.data array me pahla item summary, dusra keywords etc. hota hai
    resultDiv.innerText = "Summary:\n" + json.data[0] + "\n\nKeywords:\n" + json.data[1];
  } catch (err) {
    resultDiv.innerText = "Error contacting summarizer backend.";
  }
};
