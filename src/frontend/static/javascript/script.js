// BIBLE DICTIONARY DATA

// Data for Bible books and chapters
const bibleData = JSON.parse(document.getElementById('bibleDataJSON').textContent);
const bookNames = JSON.parse(document.getElementById('bookNamesJSON').textContent);





// SET THE SCREEN SIZE

function adjustMainWidth()
{
    const notesWidth = document.getElementById('notes').offsetWidth;
    const main = document.getElementById('main');
    main.style.width = `calc(100vw - ${notesWidth}px)`;
}

// Adjust on page load
adjustMainWidth();

// Adjust on window resize
window.addEventListener('resize', adjustMainWidth);





// CANVAS AND OTHER DATA

const staticContainer = document.querySelector('.static-container');
// const staticContainerHeight = staticContainer.offsetHeight; // May cause issues if called before DOM is fully ready and styled
let staticContainerHeight = 0; // Initialize and set later
const scrollableParagraph = document.querySelector('.scrollable-paragraph');
const canvas = document.getElementById("drawing-canvas");
const ctx = canvas.getContext("2d");
const toggleDrawing = document.getElementById("toggle-drawing");





// BIBLE DROPDOWN SELECTION

const versionSelect = document.getElementById("version");
const bookSelect = document.getElementById("book");
const chapterSelect = document.getElementById("chapter");

// These will be initialized in DOMContentLoaded from window.INITIAL_ values
let currentBook = '';
let currentChapter = '';
let currentVersion = '';

// Function to populate chapters, to be called after currentBook and currentChapter are set
function populateChapters() {
    const chapters = bibleData[currentBook];
    chapterSelect.innerHTML = '<option value="">0</option>'; // Clear existing chapter options
    if (chapters) {
        for (let i = 1; i <= chapters; i++) {
            const option = document.createElement("option");
            option.value = i;
            option.textContent = `${i}`;
            if (i.toString() === currentChapter) {
                option.selected = true;
            }
            chapterSelect.appendChild(option);
        }
    } else {
        // If for some reason currentBook isn't in bibleData, or has no chapters
        chapterSelect.innerHTML = '<option value="">N/A</option>';
    }
    // Ensure the select element reflects the currentChapter value if it was set
    if (currentChapter && chapterSelect.value !== currentChapter) {
        chapterSelect.value = currentChapter;
    }
}

// Populate chapter dropdown based on Book selection
bookSelect.addEventListener("change", function() {
    currentBook = this.value;
    // When book changes, chapter should reset or go to 1 by default if we want immediate navigation
    // For now, just repopulate and let user pick. Or, set to 1 and navigate?
    // Let's assume the chapter change listener will handle navigation.
    currentChapter = "1"; // Default to chapter 1 of the new book before populating
    populateChapters();
    // Optionally, navigate immediately to chapter 1 of the new book:
    // window.location.href = `/${currentBook}-1-${currentVersion}`;
});

// Redirect on Chapter selection
chapterSelect.addEventListener("change", function() {
    const selectedBook = bookSelect.value; // or currentBook
    const selectedChapter = this.value;
    const selectedVersion = versionSelect.value; // or currentVersion

    if (selectedBook && selectedChapter && selectedChapter !== "0" && selectedChapter !== "") {
        window.location.href = `/${selectedBook}-${selectedChapter}-${selectedVersion}`;
    }
});

// Redirect on Version selection
versionSelect.addEventListener("change", function() {
    const selectedVersion = this.value;
    const selectedBook = bookSelect.value; // or currentBook
    const selectedChapter = chapterSelect.value; // or currentChapter

    if (selectedVersion && selectedBook && selectedChapter && selectedChapter !== "0" && selectedChapter !== "") {
        window.location.href = `/${selectedBook}-${selectedChapter}-${selectedVersion}`;
    }
});





// SELECTION OF TEXT

// Function to enable all buttons in #highlightButtons
function enableButtons()
{
    const buttons = document.querySelectorAll('#highlightButtons button');
    buttons.forEach(button => button.disabled = false);
}
function disableButtons()
{
    const buttons = document.querySelectorAll('#highlightButtons button');
    buttons.forEach(button => button.disabled = true);
}

// Initialize selected data variable
var selectedText = "";
var persistText = "";

document.addEventListener("mouseup", (event) => {
    handleTouch(event);
});
document.addEventListener("touchend", (event) => {
    handleTouch(event);
});

document.addEventListener("mousedown", (event) => {
    // popup.style.display = "none";
    disableButtons();
});
document.addEventListener("touchstart", (event) => {
    // popup.style.display = "none";
    disableButtons();
});

function handleTouch(event)
{
    // Get the selected text
    selectedText = document.getSelection();

    if (selectedText.toString() !== "") { // check if selectedText is not an empty string

        // Show the popup near the selection
        persistText = selectedText;
        enableButtons();

        // popup.style.display = "block";
        // popup.style.left = `${event.pageX}px`;
        // popup.style.top = `${event.pageY}px`;
    }
    else
    {
        // popup.style.display = "none";
        disableButtons();
    }
}

// EXPLAIN
explainButton.addEventListener("mousedown", () => {
    // popup.style.display = "none";
    handleExplain(); // Prevent clearing selection
});
explainButton.addEventListener("touchstart", () => {
    // popup.style.display = "none";
    handleExplain(); // Prevent clearing selection
});

// DEFINE
defineButton.addEventListener("mousedown", () => {
    // popup.style.display = "none";
    handleDefine(); // Prevent clearing selection
});
defineButton.addEventListener("touchstart", () => {
    // popup.style.display = "none";
    handleDefine(); // Prevent clearing selection
});

// QUESTION
questionButton.addEventListener("mousedown", () => {
    // popup.style.display = "none";
    handleQuestion(); // Prevent clearing selection
});
questionButton.addEventListener("touchstart", () => {
    // popup.style.display = "none";
    handleQuestion(); // Prevent clearing selection
});

// SELECTED QUESTION
selectedQuestionButton.addEventListener("mousedown", () => {
    // popup.style.display = "none";
    handleSelectedQuestion(); // Prevent clearing selection
});
selectedQuestionButton.addEventListener("touchstart", () => {
    // popup.style.display = "none";
    handleSelectedQuestion(); // Prevent clearing selection
});

// CROSS REFERENCE
crossReferenceButton.addEventListener("mousedown", () => {
    // popup.style.display = "none";
    handleCrossReference(); // Prevent clearing selection
});
crossReferenceButton.addEventListener("touchstart", () => {
    // popup.style.display = "none";
    handleCrossReference(); // Prevent clearing selection
});

// QUIZ
quizButton.addEventListener("mousedown", () => {
    // popup.style.display = "none";
    handleQuiz(); // Prevent clearing selection
});
quizButton.addEventListener("touchstart", () => {
    // popup.style.display = "none";
    handleQuiz(); // Prevent clearing selection
});

// SUMMARIZE
chapterSummaryButton.addEventListener("mousedown", () => {
    // popup.style.display = "none";
    summarizeChapter(); // Prevent clearing selection
});
chapterSummaryButton.addEventListener("touchstart", () => {
    // popup.style.display = "none";
    summarizeChapter(); // Prevent clearing selection
});

// IMAGES
imageButton.addEventListener("mousedown", () => {
    // popup.style.display = "none";
    handleImages(); // Prevent clearing selection
});
imageButton.addEventListener("touchstart", () => {
    // popup.style.display = "none";
    handleImages(); // Prevent clearing selection
});

// MAP
mapButton.addEventListener("mousedown", () => {
    // popup.style.display = "none";
    handleMap(); // Prevent clearing selection
});
mapButton.addEventListener("touchstart", () => {
    // popup.style.display = "none";
    handleMap(); // Prevent clearing selection
});





// EXPLAIN TEXT
// Explain selected data
function handleExplain()
{
    if (persistText.toString())
    {
        alert("Please be patient as your response generates.")
        const range = persistText.getRangeAt(0);
        const parentElement = range.startContainer.parentElement;

        // Traverse up to find the closest element with an ID
        const elementWithID = parentElement.closest('[id]');
        var fullNodeContentText = "";

        if(elementWithID)
        {
            fullNodeContentText = elementWithID.textContent;
        }

        // Send the selected text to the server
        fetch('/api/explain_selection/',
        {
            method: 'POST',
            headers:
            {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ selected_text: selectedText.toString(), full_context: fullNodeContentText, book: bookSelect.value, chapter: chapterSelect.value })
        })
        // Get JSON from the server's response
        .then(response => response.json())
        // Get the "message" key from the server's JSON response
        .then(data =>
        {
            // selectedText.empty();
            // selectedText.removeAllRanges();
            alert(data.message);
        })
        // Display error message to user if something went wrong with POST request
        .catch(error =>
        {
            console.error('Error:', error);
        });

    // Make sure the user selected some text
    }
    else
    {
        alert("Please highlight some text before clicking the button.");
    }
}





// DEFINING TEXT
// Define selected data
function handleDefine()
{
    if (persistText.toString())
    {
        alert("Please be patient as your response generates.")
        const range = persistText.getRangeAt(0);
        const parentElement = range.startContainer.parentElement;

        // Traverse up to find the closest element with an ID
        const elementWithID = parentElement.closest('[id]');
        var fullNodeContentText = "";

        if(elementWithID)
        {
            fullNodeContentText = elementWithID.textContent;
        }

        // Send the selected text to the server
        fetch('/api/define_selection/',
        {
            method: 'POST',
            headers:
            {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ selected_text: selectedText.toString(), full_context: fullNodeContentText, book: bookSelect.value, chapter: chapterSelect.value })
        })
        // Get JSON from the server's response
        .then(response => response.json())
        // Get the "message" key from the server's JSON response
        .then(data =>
        {
            // selectedText.empty();
            // selectedText.removeAllRanges();
            alert(data.message);
        })
        // Display error message to user if something went wrong with POST request
        .catch(error =>
        {
            console.error('Error:', error);
        });
    // Make sure the user selected some text
    }
    else
    {
        alert("Please highlight some text before clicking the button.");
    }
}





// ASKING QUESTION
// Define selected data
function handleQuestion()
{
    let question = prompt("Ask any question!");
    if (question != null && question != "")
    {
        alert("Please be patient as your response generates.")
        // Send the selected text to the server
        fetch('/api/ask_question/',
        {
            method: 'POST',
            headers:
            {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ user_query: question.toString()})
        })
        // Get JSON from the server's response
        .then(response => response.json())
        // Get the "message" key from the server's JSON response
        .then(data =>
        {
            // selectedText.empty();
            // selectedText.removeAllRanges();
            alert(data.message);
        })
        // Display error message to user if something went wrong with POST request
        .catch(error =>
        {
            console.error('Error:', error);
        });
    // Make sure the user selected some text
    }
    else if (question == "")
    {
        alert("Please type something in the question box.");
    }
}





// SELECTED ASKING QUESTION
// Ask selected data
function handleSelectedQuestion()
{
    if (persistText.toString())
    {
        let question = prompt("Ask any question about the selected text!");
        if (question != null && question != "")
        {
            alert("Please be patient as your response generates.")
            const range = persistText.getRangeAt(0);
            const parentElement = range.startContainer.parentElement;

            // Traverse up to find the closest element with an ID
            const elementWithID = parentElement.closest('[id]');
            var fullNodeContentText = "";

            if(elementWithID)
            {
                fullNodeContentText = elementWithID.textContent;
            }

            // Send the selected text to the server
            fetch('/api/ask_selection/',
            {
                method: 'POST',
                headers:
                {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({user_query: question.toString(), selected_text: selectedText.toString(), full_context: fullNodeContentText, book: bookSelect.value, chapter: chapterSelect.value })
            })
            // Get JSON from the server's response
            .then(response => response.json())
            // Get the "message" key from the server's JSON response
            .then(data =>
            {
                // selectedText.empty();
                // selectedText.removeAllRanges();
                alert(data.message);
            })
            // Display error message to user if something went wrong with POST request
            .catch(error =>
            {
                console.error('Error:', error);
            });
        }
        else if (question == "")
        {
            alert("Please type something in the question box.");
        }
    // Make sure the user selected some text
    }
    else
    {
        alert("Please highlight some text before clicking the button.");
    }
}




// CROSS REFERENCE
// Cross reference selected data
function handleCrossReference()
{
    if (persistText.toString())
    {
        alert("Please be patient as your response generates.")

        // Send the selected text to the server
        fetch('/api/cross_reference/',
        {
            method: 'POST',
            headers:
            {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ selected_text: selectedText.toString()})
        })
        // Get JSON from the server's response
        .then(response => response.json())
        // Get the "message" key from the server's JSON response
        .then(data =>
        {
            // selectedText.empty();
            // selectedText.removeAllRanges();
            alert(data.message);
        })
        // Display error message to user if something went wrong with POST request
        .catch(error =>
        {
            console.error('Error:', error);
        });
    
        // Make sure the user selected some text
    }
    else
    {
        alert("Please highlight some text before clicking the button.");
    }
}





// QUIZ
// Select all <p> elements on the page
function handleQuiz()
{
    const paragraphs = document.querySelectorAll('p');

    // Extract and store the text content of each <p> element
    const paragraphContents = Array.from(paragraphs).map(p => p.textContent);

    alert("WARNING: Quiz questions and options may be inaccurate.");
    alert("Please wait while your quiz generates.");

    let results = {};
    let quizData = {};

    // Fetch the quiz data from the server
    fetch('/api/get_quiz/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ full_context: paragraphContents })
    })
    .then(response => response.json())
    .then(data => {
        // alert(data.message);

        // Parse the JSON response
        try {
            quizData = data.message;
            // alert(quizData);
        }
        catch (error) {
            // Handle the error
            alert("Quiz could not be generated. Please try again.")
            console.error("An error occurred:", error.message);
            return;
        }

        // Create or show the modal for the quiz
        let modal = document.getElementById('quizModal');
        if (!modal) {
            modal = document.createElement('div');
            modal.id = 'quizModal';
            modal.className = 'modal-overlay';

            const modalContent = document.createElement('div');
            modalContent.className = 'modal-content';

            const closeBtn = document.createElement('span');
            closeBtn.className = 'modal-close-btn';
            closeBtn.innerHTML = '&times;';
            closeBtn.onclick = () => { modal.remove() };

            const quizContainer = document.createElement('form');
            quizContainer.id = 'quizForm';

            const submitButton = document.createElement('button');
            submitButton.type = 'button';
            submitButton.textContent = 'Submit Quiz';
            submitButton.onclick = () => {
                // Gather quiz answers
                const formData = new FormData(quizContainer);
                results = {};
                for (const [key, value] of formData.entries()) {
                    results[key] = value;
                }

                // Send results to the server
                fetch('/api/submit_quiz/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ quiz_results: results, quiz_answers: quizData })
                })
                .then(response => response.json())
                .then(serverResponse => {
                    alert(serverResponse.message);
                })
                .catch(error => {
                    console.error('Error submitting quiz:', error);
                });
            };

            modalContent.appendChild(closeBtn);
            modalContent.appendChild(quizContainer);
            modalContent.appendChild(submitButton);
            modal.appendChild(modalContent);
            document.body.appendChild(modal);
        }

        const quizContainer = modal.querySelector('#quizForm');
        quizContainer.innerHTML = ''; // Clear previous quiz content

        // Populate the quiz with questions and options
        Object.entries(quizData).forEach(([question, details], index) => {
            // Create a container for each question
            const questionDiv = document.createElement('div');
            questionDiv.className = 'quiz-question';

            // Add question text
            const questionTitle = document.createElement('p');
            questionTitle.textContent = `${index + 1}. ${question}`;
            questionDiv.appendChild(questionTitle);

            // Add options as radio buttons
            Object.entries(details.options).forEach(([key, value]) => {
                const label = document.createElement('label');
                label.textContent = value;

                const radioInput = document.createElement('input');
                radioInput.type = 'radio';
                radioInput.name = question; // Group options under the same question
                radioInput.value = key;

                label.prepend(radioInput); // Add radio button before the text
                questionDiv.appendChild(label);
                questionDiv.appendChild(document.createElement('br'));
            });

            quizContainer.appendChild(questionDiv);
        });
        modal.style.display = 'flex'; // Show the modal
    })
    .catch(error => {
        console.error('Error fetching quiz:', error);
    });
}




// SUMMARIZE CHAPTER
// Select all <p> elements on page for full context
function summarizeChapter()
{
    const paragraphs = document.querySelectorAll('p');

    // Extract and store the text content of each <p> element
    const paragraphContents = Array.from(paragraphs).map(p => p.textContent);

    alert("Please be patient as your response generates.")
    // Send the selected text to the server
    fetch('/api/summarize_chapter/',
    {
        method: 'POST',
        headers:
        {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ full_context: paragraphContents, book: bookSelect.value, chapter: chapterSelect.value })
    })
    // Get JSON from the server's response
    .then(response => response.json())
    // Get the "message" key from the server's JSON response
    .then(data =>
    {
        // selectedText.empty();
        // selectedText.removeAllRanges();
        alert(data.message);
    })
    // Display error message to user if something went wrong with POST request
    .catch(error =>
    {
        console.error('Error:', error);
    });
}





// IMAGES
// search for a map of selected data
function handleImages()
{
    if (persistText.toString()) {
        // Send the selected text to the server
        fetch('/api/search_selection/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ selected_text: persistText.toString() })
        })
        .then(response => response.json())
        .then(data => {
            if (data.images && data.images.length > 0) {
                // Create the modal container if it doesn't already exist
                let modal = document.getElementById('imageModal');
                if (!modal) {
                    modal = document.createElement('div');
                    modal.id = 'imageModal';
                    modal.className = 'modal-overlay';

                    // Modal content container
                    const modalContent = document.createElement('div');
                    modalContent.className = 'modal-content';

                    // Close button
                    const closeBtn = document.createElement('span');
                    closeBtn.className = 'modal-close-btn';
                    closeBtn.innerHTML = '&times;';
                    closeBtn.onclick = () => { modal.style.display = 'none'; };

                    // Image container
                    const imageContainer = document.createElement('div');
                    imageContainer.className = 'modal-image-container';

                    // Append elements to modal
                    modalContent.appendChild(closeBtn);
                    modalContent.appendChild(imageContainer);
                    modal.appendChild(modalContent);
                    document.body.appendChild(modal);
                }

                // Clear any previous images
                const imageContainer = modal.querySelector('.modal-image-container');
                imageContainer.innerHTML = '';

                // Populate modal with images from data
                data.images.forEach(url => {
                    const img = document.createElement('img');
                    img.src = url;
                    img.alt = 'Gallery Image';
                    img.className = 'modal-image';
                    imageContainer.appendChild(img);
                });

                // Show the modal
                modal.style.display = 'flex';

                selectedText.empty();
                selectedText.removeAllRanges();
            } else {
                alert("No images found. Please try again later.");
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    } else {
        alert("Please highlight some text before clicking the button.");
    }
}





// MAP
// search for a map of selected data
function handleMap()
{
    if (persistText.toString()) {
        // Send the selected text to the server
        fetch('/api/search_map_selection/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ selected_text: persistText.toString() })
        })
        .then(response => response.json())
        .then(data => {
            if (data.images && data.images.length > 0) {
                // Create the modal container if it doesn't already exist
                let modal = document.getElementById('imageModal');
                if (!modal) {
                    modal = document.createElement('div');
                    modal.id = 'imageModal';
                    modal.className = 'modal-overlay';

                    // Modal content container
                    const modalContent = document.createElement('div');
                    modalContent.className = 'modal-content';

                    // Close button
                    const closeBtn = document.createElement('span');
                    closeBtn.className = 'modal-close-btn';
                    closeBtn.innerHTML = '&times;';
                    closeBtn.onclick = () => { modal.style.display = 'none'; };

                    // Image container
                    const imageContainer = document.createElement('div');
                    imageContainer.className = 'modal-image-container';

                    // Append elements to modal
                    modalContent.appendChild(closeBtn);
                    modalContent.appendChild(imageContainer);
                    modal.appendChild(modalContent);
                    document.body.appendChild(modal);
                }

                // Clear any previous images
                const imageContainer = modal.querySelector('.modal-image-container');
                imageContainer.innerHTML = '';

                // Populate modal with images from data
                data.images.forEach(url => {
                    const img = document.createElement('img');
                    img.src = url;
                    img.alt = 'Gallery Image';
                    img.className = 'modal-image';
                    imageContainer.appendChild(img);
                });

                // Show the modal
                modal.style.display = 'flex';

                selectedText.empty();
                selectedText.removeAllRanges();
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    } else {
        alert("Please highlight some text before clicking the button.");
    }
}








// HIGHLIGHTING TEXT

document.getElementById('highlightButton').addEventListener('click', () =>
{
    if (selectedText.toString())
    {
        const range = selectedText.getRangeAt(0);
        const selectedIDs = new Set();

        // Clone the range content to find all selected <p> elements
        const nodes = range.cloneContents().querySelectorAll('p');

        nodes.forEach(node =>
        {
            if (node.id)
            {
                selectedIDs.add(node.id); // Add the id to the set if it exists
            }
        });

        // If specific paragraphs are selected
        if (selectedIDs.size > 0)
        {
            selectedIDs.forEach(id =>
            {
                const element = document.getElementById(id);
                const elementRange = document.createRange();

                // Determine if only part of the paragraph is selected
                if (element.contains(range.startContainer) || element.contains(range.endContainer))
                {
                    const span = document.createElement("span");
                    span.className = "highlight";

                    // Adjust the range to highlight only the selected portion
                    if (element.contains(range.startContainer))
                    {
                        elementRange.setStart(range.startContainer, range.startOffset);
                    }
                    else
                    {
                        elementRange.setStart(element, 0);
                    }

                    if (element.contains(range.endContainer))
                    {
                        elementRange.setEnd(range.endContainer, range.endOffset);
                    }
                    else
                    {
                        elementRange.setEnd(element, element.childNodes.length);
                    }

                    // Wrap the selected content in a span
                    const extractedContent = elementRange.extractContents();
                    span.appendChild(extractedContent);
                    elementRange.insertNode(span);
                }
                else
                {
                    // If the whole paragraph is selected, wrap entire content
                    element.innerHTML = `<span class="highlight">${element.innerHTML}</span>`;
                }
            });
        }
        else
        {
            // If only a single range within a single paragraph is selected
            const span = document.createElement("span");
            span.className = "highlight";
            range.surroundContents(span);
        }

        // Clear the selection after highlighting
        selectedText.removeAllRanges();

    }
    else
    {
        alert("Please select some text to highlight.");
    }
});

// Maintain highlighted content data while mouse clicking on highlight button to prevent internal deselection
highlightButton.addEventListener('mousedown', (e) =>
{
    // Prevent the button from clearing the selection
    e.preventDefault();
});

// Maintain highlighted content data while screen tapping on highlight button to prevent internal deselection
highlightButton.addEventListener('touchbegin', (e) =>
{
    // Prevent the button from clearing the selection
    e.preventDefault();
});




// DRAWING

// Set canvas size to match the expanding div size
canvas.width = scrollableParagraph.clientWidth;
canvas.height = scrollableParagraph.scrollHeight;

window.addEventListener("resize", () => {
    canvas.width = scrollableParagraph.clientWidth;
    canvas.height = scrollableParagraph.scrollHeight;
});

let isDrawing = false;
let lastX = 0;
let lastY = 0;

// Function to start drawing on PC
canvas.addEventListener("mousedown", (e) => {
    isDrawing = true;
    const rect = canvas.getBoundingClientRect();
    lastX = e.clientX - rect.left;
    lastY = e.clientY - rect.top;
});

canvas.addEventListener("mouseup", () => isDrawing = false);
canvas.addEventListener("mouseout", () => isDrawing = false);

// Function to draw on the canvas
canvas.addEventListener("mousemove", (e) => {
    if (!isDrawing) return;

    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    ctx.strokeStyle = "#FF0000"; // Set drawing color
    ctx.lineWidth = 2; // Set line width
    ctx.lineJoin = "round";
    ctx.lineCap = "round";

    ctx.beginPath();
    ctx.moveTo(lastX, lastY);
    ctx.lineTo(x, y);
    ctx.stroke();

    lastX = x;
    lastY = y;
});

// Add touch equivalents for mobile devices
canvas.addEventListener("touchstart", (e) => {
    isDrawing = true;
    const rect = canvas.getBoundingClientRect();
    lastX = e.touches[0].clientX - rect.left;
    lastY = e.touches[0].clientY - rect.top;
    e.preventDefault(); // Prevent scrolling
});

canvas.addEventListener("touchend", () => isDrawing = false);
canvas.addEventListener("touchcancel", () => isDrawing = false);

canvas.addEventListener("touchmove", (e) => {
    if (!isDrawing) return;

    const rect = canvas.getBoundingClientRect();
    const x = e.touches[0].clientX - rect.left;
    const y = e.touches[0].clientY - rect.top;

    ctx.strokeStyle = "#FF0000"; // Set drawing color
    ctx.lineWidth = 2; // Set line width
    ctx.lineJoin = "round";
    ctx.lineCap = "round";

    ctx.beginPath();
    ctx.moveTo(lastX, lastY);
    ctx.lineTo(x, y);
    ctx.stroke();

    lastX = x;
    lastY = y;
    e.preventDefault(); // Prevent scrolling
});

// Toggle drawing mode
toggleDrawing.addEventListener("change", () => {
    if (toggleDrawing.checked) {
        // Enable pointer events for drawing and add event listeners for mouse and touch events
        canvas.style.pointerEvents = "auto";
        canvas.addEventListener("mousedown", startDrawing);
        canvas.addEventListener("mousemove", draw);
        canvas.addEventListener("mouseup", stopDrawing);
        canvas.addEventListener("mouseout", stopDrawing);

        canvas.addEventListener("touchstart", startDrawing);
        canvas.addEventListener("touchmove", draw);
        canvas.addEventListener("touchend", stopDrawing);
        canvas.addEventListener("touchcancel", stopDrawing);
    } else {
        // Disable pointer events to prevent further drawing but retain the drawing on canvas
        canvas.style.pointerEvents = "none";

        // Remove event listeners for mouse and touch events
        canvas.removeEventListener("mousedown", startDrawing);
        canvas.removeEventListener("mousemove", draw);
        canvas.removeEventListener("mouseup", stopDrawing);
        canvas.removeEventListener("mouseout", stopDrawing);

        canvas.removeEventListener("touchstart", startDrawing);
        canvas.removeEventListener("touchmove", draw);
        canvas.removeEventListener("touchend", stopDrawing);
        canvas.removeEventListener("touchcancel", stopDrawing);
    }
});





// FORWARD AND BACK BUTTONS

// Initialize navigation variables (Done globally now, set in DOMContentLoaded)
// let currentBook = bookSelect.value;
// let currentChapter = chapterSelect.value;
// let currentVersion = versionSelect.value;

// Next button click event for all elements with class 'nextButton'
document.querySelectorAll('.nextButton').forEach(button => {
    button.addEventListener('click', () => {
        const totalChapters = bibleData[currentBook];
        let chapterNumber = parseInt(currentChapter, 10);


        if (chapterNumber < totalChapters) {
            // Move to the next chapter within the same book
            chapterNumber++;
        } else {
            // Move to the first chapter of the next book
            const currentBookIndex = bookNames.indexOf(currentBook);
            const nextBookIndex = (currentBookIndex + 1) % bookNames.length; // Wrap around to Genesis if at the end
            currentBook = bookNames[nextBookIndex];
            chapterNumber = 1;
        }
        currentChapter = chapterNumber.toString();


        // Update display
        window.location.href = `/${currentBook}-${currentChapter}-${currentVersion}`;
    });
});

// Previous button click event for all elements with class 'previousButton'
document.querySelectorAll('.previousButton').forEach(button => {
    button.addEventListener('click', () => {
        let chapterNumber = parseInt(currentChapter, 10);
        if (chapterNumber > 1) {
            // Move to the previous chapter within the same book
            chapterNumber--;
        } else {
            // Move to the last chapter of the previous book
            const currentBookIndex = bookNames.indexOf(currentBook);
            const previousBookIndex = (currentBookIndex - 1 + bookNames.length) % bookNames.length; // Wrap around to Revelation if at the beginning
            currentBook = bookNames[previousBookIndex];
            chapterNumber = bibleData[currentBook]; // Set to last chapter of the previous book
        }
        currentChapter = chapterNumber.toString();


        // Update display
        window.location.href = `/${currentBook}-${currentChapter}-${currentVersion}`;
    });
});

// Helper functions for drawing (assuming these were defined elsewhere or were intended to be)
function startDrawing(e) {
    isDrawing = true;
    const rect = canvas.getBoundingClientRect();
    if (e.touches) {
        lastX = e.touches[0].clientX - rect.left;
        lastY = e.touches[0].clientY - rect.top;
        e.preventDefault(); // Prevent scrolling
    } else {
        lastX = e.clientX - rect.left;
        lastY = e.clientY - rect.top;
    }
}

function draw(e) {
    if (!isDrawing) return;
    const rect = canvas.getBoundingClientRect();
    let x, y;
    if (e.touches) {
        x = e.touches[0].clientX - rect.left;
        y = e.touches[0].clientY - rect.top;
        e.preventDefault(); // Prevent scrolling
    } else {
        x = e.clientX - rect.left;
        y = e.clientY - rect.top;
    }

    ctx.strokeStyle = "#FF0000"; // Set drawing color
    ctx.lineWidth = 2; // Set line width
    ctx.lineJoin = "round";
    ctx.lineCap = "round";

    ctx.beginPath();
    ctx.moveTo(lastX, lastY);
    ctx.lineTo(x, y);
    ctx.stroke();

    lastX = x;
    lastY = y;
}

function stopDrawing() {
    isDrawing = false;
}

// Ensure the DOM is fully loaded before initializing dropdowns and current values
document.addEventListener('DOMContentLoaded', () => {
    staticContainerHeight = staticContainer.offsetHeight; // Set this after DOM is ready

    // Set initial values from global variables provided by the HTML template
    if (typeof window.INITIAL_BOOK !== 'undefined') {
        currentBook = window.INITIAL_BOOK;
        bookSelect.value = currentBook; // Ensure select reflects this, though Jinja should have by 'selected'
    }
    if (typeof window.INITIAL_CHAPTER !== 'undefined') {
        currentChapter = window.INITIAL_CHAPTER.toString();
        // chapterSelect.value will be set after options are populated
    }
    if (typeof window.INITIAL_VERSION !== 'undefined') {
        currentVersion = window.INITIAL_VERSION;
        versionSelect.value = currentVersion; // Ensure select reflects this
    }

    // Populate chapters for the initially selected book and set the correct chapter
    populateChapters();
}); 