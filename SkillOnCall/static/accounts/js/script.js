document.addEventListener('DOMContentLoaded', function () {
    // Toggle provider fields
    const userTypeSelect = document.getElementById('userTypeSelect');
    const providerFields = document.getElementById('providerFields');
    
    userTypeSelect.addEventListener('change', function() {
        providerFields.style.display = this.value === 'provider' ? 'block' : 'none';
    });
    
    // Image preview
    window.previewImage = function(input, previewId) {
        const preview = document.getElementById(previewId);
        const file = input.files[0];
        const reader = new FileReader();
        
        reader.onload = function(e) {
            if (preview.tagName === 'IMG') {
                preview.src = e.target.result;
            } else {
                const img = document.createElement('img');
                img.src = e.target.result;
                img.className = 'rounded-circle shadow';
                img.width = 100;
                img.height = 100;
                img.alt = 'Profile picture';
                preview.replaceWith(img);
                img.id = previewId;
            }
        }
        
        if (file) {
            reader.readAsDataURL(file);
        }
    }
});
