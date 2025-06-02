document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('contentForm');
    const statusDiv = document.getElementById('status');
    const statusMessage = document.getElementById('status-message');
    const progressBar = document.getElementById('progress-bar');
    const progressPercentage = document.getElementById('progress-percentage');
    const resultDiv = document.getElementById('result');
    const resultContent = document.getElementById('result-content');
    const feedbackSection = document.getElementById('feedbackSection');
    const toast = document.getElementById('toast');
    const toastMessage = document.getElementById('toast-message');
    const elapsedTimeElement = document.getElementById('elapsed-time');
    let socket;
    let startTime;
    let elapsedTimeInterval;

    // Toast notification function
    function showToast(message, type = 'info') {
        toastMessage.textContent = message;
        toast.className = `toast show ${type}`;
        setTimeout(() => {
            toast.className = 'toast';
        }, 3000);
    }

    // Update elapsed time
    function updateElapsedTime() {
        const now = new Date();
        const elapsed = Math.floor((now - startTime) / 1000);
        const minutes = Math.floor(elapsed / 60);
        const seconds = elapsed % 60;
        elapsedTimeElement.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }

    // Start timer
    function startTimer() {
        startTime = new Date();
        elapsedTimeInterval = setInterval(updateElapsedTime, 1000);
    }

    // Stop timer
    function stopTimer() {
        if (elapsedTimeInterval) {
            clearInterval(elapsedTimeInterval);
        }
    }

    // Copy content to clipboard
    window.copyContent = async () => {
        const content = resultContent.textContent;
        try {
            await navigator.clipboard.writeText(content);
            showToast('Content copied to clipboard!', 'success');
        } catch (err) {
            showToast('Failed to copy content', 'error');
        }
    };

    // Show feedback form
    window.showFeedbackForm = () => {
        feedbackSection.classList.remove('hidden');
        feedbackSection.scrollIntoView({ behavior: 'smooth' });
    };

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Reset UI
        statusDiv.classList.remove('hidden');
        resultDiv.classList.add('hidden');
        feedbackSection.classList.add('hidden');
        progressBar.style.width = '0%';
        progressPercentage.textContent = '0%';
        statusMessage.textContent = 'Starting content generation...';
        document.getElementById('log-entries').innerHTML = '';
        
        // Start timer
        startTimer();

        // Create FormData
        const formData = new FormData(form);

        try {
            // Send request
            const response = await fetch('/generate', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Generation failed');
            }

            const data = await response.json();
            
            // Connect to WebSocket
            socket = new WebSocket(`ws://${window.location.host}${data.websocket_url}`);
            
            socket.onmessage = (event) => {
                const status = JSON.parse(event.data);
                const logEntries = document.getElementById('log-entries');
                
                // Update status message
                statusMessage.textContent = status.message;

                // Add log entry with animation
                if (status.message) {
                    const logEntry = document.createElement('div');
                    logEntry.className = 'log-entry p-4 bg-white rounded-lg shadow-sm border border-gray-100';
                    
                    let logContent = `
                        <div class="flex items-start space-x-3">
                            <div class="flex-shrink-0">
                                <i class="fas ${status.type === 'error' ? 'fa-exclamation-circle text-red-500' : 'fa-info-circle text-blue-500'}"></i>
                            </div>
                            <div class="flex-1 min-w-0">
                                <p class="text-sm font-medium text-gray-900">${status.message}</p>
                    `;
                    
                    if (status.agent) {
                        logContent += `
                            <div class="mt-1 flex items-center text-xs text-gray-500">
                                <i class="fas fa-robot mr-1"></i>
                                <span>Agent: ${status.agent}</span>
                            </div>
                        `;
                    }
                    
                    if (status.timestamp) {
                        logContent += `
                            <div class="mt-1 flex items-center text-xs text-gray-500">
                                <i class="far fa-clock mr-1"></i>
                                <span>${new Date(status.timestamp).toLocaleTimeString()}</span>
                            </div>
                        `;
                    }
                    
                    if (status.output) {
                        logContent += `
                            <div class="mt-2 p-3 bg-gray-50 rounded-md">
                                <pre class="text-xs text-gray-700 whitespace-pre-wrap">${status.output}</pre>
                            </div>
                        `;
                    }
                    
                    logContent += `</div></div>`;
                    logEntry.innerHTML = logContent;
                    logEntries.appendChild(logEntry);
                    logEntries.scrollTop = logEntries.scrollHeight;
                }

                // Update progress bar for different event types
                let progress = 0;
                switch (status.type) {
                    case 'task_started':
                        progress = 33;
                        break;
                    case 'task_completed':
                        progress = 66;
                        break;
                    case 'completed':
                        progress = 100;
                        progressBar.style.width = '100%';
                        progressPercentage.textContent = '100%';
                        // Show results
                        resultDiv.classList.remove('hidden');
                        resultContent.textContent = status.result;
                        showToast('Content generated successfully', 'success');
                        stopTimer();
                        socket.close();
                        break;
                    case 'error':
                        statusMessage.classList.add('text-red-600');
                        progressBar.classList.add('bg-red-600');
                        showToast('An error occurred during generation', 'error');
                        stopTimer();
                        socket.close();
                        break;
                }
                
                if (progress > 0) {
                    progressBar.style.width = `${progress}%`;
                    progressPercentage.textContent = `${progress}%`;
                }
            };

            socket.onerror = (error) => {
                console.error('WebSocket error:', error);
                statusMessage.textContent = 'Connection error occurred';
                statusMessage.classList.add('text-red-600');
                showToast('Connection error occurred', 'error');
                stopTimer();
            };

        } catch (error) {
            console.error('Error:', error);
            statusMessage.textContent = 'Error generating content: ' + error.message;
            statusMessage.classList.add('text-red-600');
            showToast('Error generating content', 'error');
            stopTimer();
        }
    });
});
