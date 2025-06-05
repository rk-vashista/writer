// Function to handle platform selection changes
function handlePlatformChange(platform) {
    const githubFields = document.getElementById('githubFields');
    const contentTypeSelect = document.getElementById('content-type-select');
    
    // Show/hide GitHub-specific fields
    if (githubFields) {
        if (platform === 'github') {
            githubFields.classList.remove('hidden');
        } else {
            githubFields.classList.add('hidden');
        }
    }

    // Handle content type options
    if (contentTypeSelect) {
        const options = contentTypeSelect.options;
        for (let i = 0; i < options.length; i++) {
            const option = options[i];
            const type = option.getAttribute('data-type');
            
            if (type === 'all' || 
                (platform === 'github' && type === 'github') || 
                (platform !== 'github' && type === 'regular')) {
                option.style.display = '';
            } else {
                option.style.display = 'none';
            }
        }
        contentTypeSelect.value = '';
    }
}

// Function to toggle GitHub token visibility
function toggleTokenVisibility() {
    const tokenInput = document.getElementById('githubToken');
    const tokenIcon = document.getElementById('tokenVisibilityIcon');
    if (tokenInput.type === 'password') {
        tokenInput.type = 'text';
        tokenIcon.classList.remove('fa-eye');
        tokenIcon.classList.add('fa-eye-slash');
    } else {
        tokenInput.type = 'password';
        tokenIcon.classList.remove('fa-eye-slash');
        tokenIcon.classList.add('fa-eye');
    }
}



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
        const rawContent = document.getElementById('raw-content');
        try {
            await navigator.clipboard.writeText(rawContent.textContent);
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
                        const rawContent = document.getElementById('raw-content');
                        rawContent.textContent = status.result;
                        
                        // Parse and render markdown
                        try {
                            // Configure marked for GitHub-flavored markdown
                            marked.setOptions({
                                gfm: true,
                                breaks: true,
                                headerIds: true,
                                mangle: false,
                                pedantic: false,
                                sanitize: false,
                                smartLists: true,
                                smartypants: true,
                                highlight: function(code, lang) {
                                    if (lang && hljs.getLanguage(lang)) {
                                        try {
                                            return hljs.highlight(code, { language: lang }).value;
                                        } catch (err) {}
                                    }
                                    return code;
                                }
                            });
                            
                            // Pre-process content for better emoji and formatting
                            let processedContent = status.result
                                // Ensure proper spacing around emojis
                                .replace(/([🎯📝📰🏷️📢🚀💡✨🔥👥📊📈📌🎨💪🌟⭐])/g, ' $1 ')
                                // Clean up extra spaces
                                .replace(/\s+/g, ' ')
                                // Ensure proper markdown formatting for special sections
                                .replace(/^(##\s*[🎯📝📰🏷️📢🚀💡✨🔥👥📊📈📌🎨💪🌟⭐])/gm, '\n$1')
                                // Add spacing after section headers
                                .replace(/^(##\s*.+)$/gm, '$1\n');
                            
                            // Parse markdown and sanitize HTML
                            const parsedContent = marked.parse(processedContent);
                            const sanitizedContent = DOMPurify.sanitize(parsedContent, {
                                ADD_TAGS: ['iframe', 'details', 'summary'],
                                ADD_ATTR: ['allow', 'allowfullscreen', 'frameborder', 'scrolling', 'open']
                            });
                            
                            // Update the content
                            resultContent.innerHTML = sanitizedContent;
                            
                            // Post-process for enhanced styling
                            resultContent.querySelectorAll('h1, h2, h3, h4, h5, h6').forEach(heading => {
                                if (heading.textContent.includes('🚀') || heading.textContent.includes('IMMEDIATE')) {
                                    heading.classList.add('highlight-box');
                                }
                            });
                            
                            // Add special styling to content sections
                            resultContent.querySelectorAll('h2').forEach(h2 => {
                                const nextSibling = h2.nextElementSibling;
                                if (nextSibling && (nextSibling.tagName === 'P' || nextSibling.tagName === 'UL' || nextSibling.tagName === 'OL')) {
                                    const wrapper = document.createElement('div');
                                    wrapper.className = 'content-section';
                                    h2.parentNode.insertBefore(wrapper, h2);
                                    wrapper.appendChild(h2);
                                    
                                    let currentElement = nextSibling;
                                    while (currentElement && currentElement.tagName !== 'H1' && currentElement.tagName !== 'H2') {
                                        const nextEl = currentElement.nextElementSibling;
                                        wrapper.appendChild(currentElement);
                                        currentElement = nextEl;
                                    }
                                }
                            });
                            
                            // Add click-to-copy for code blocks
                            resultContent.querySelectorAll('pre').forEach(block => {
                                // Create copy button
                                const copyBtn = document.createElement('button');
                                copyBtn.className = 'copy-button absolute right-2 top-2 text-xs px-2 py-1 rounded bg-gray-700 text-white opacity-0 transition-opacity hover:bg-gray-600';
                                copyBtn.innerHTML = '<i class="fas fa-copy mr-1"></i>Copy';
                                
                                // Set relative positioning on pre element
                                block.style.position = 'relative';
                                block.appendChild(copyBtn);
                                
                                // Show/hide button on hover
                                block.addEventListener('mouseenter', () => copyBtn.style.opacity = '1');
                                block.addEventListener('mouseleave', () => copyBtn.style.opacity = '0');
                                
                                // Copy functionality
                                copyBtn.addEventListener('click', async () => {
                                    const code = block.querySelector('code')?.innerText || block.innerText;
                                    await navigator.clipboard.writeText(code);
                                    copyBtn.innerHTML = '<i class="fas fa-check mr-1"></i>Copied!';
                                    setTimeout(() => {
                                        copyBtn.innerHTML = '<i class="fas fa-copy mr-1"></i>Copy';
                                    }, 2000);
                                });
                            });
                            
                            // Add target="_blank" to external links
                            resultContent.querySelectorAll('a').forEach(link => {
                                if (link.host !== window.location.host) {
                                    link.setAttribute('target', '_blank');
                                    link.setAttribute('rel', 'noopener noreferrer');
                                }
                            });
                            
                            // Initialize tooltips for links
                            resultContent.querySelectorAll('a[title]').forEach(link => {
                                link.className += ' relative group';
                                const tooltip = document.createElement('span');
                                tooltip.className = 'absolute hidden group-hover:block bg-black text-white text-xs rounded py-1 px-2 -top-8 left-1/2 transform -translate-x-1/2 whitespace-nowrap';
                                tooltip.textContent = link.title;
                                link.appendChild(tooltip);
                            });
                        } catch (e) {
                            console.error('Error rendering markdown:', e);
                            resultContent.textContent = status.result;
                        }
                        
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
