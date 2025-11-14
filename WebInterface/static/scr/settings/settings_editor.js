document.addEventListener("DOMContentLoaded", () => {
    const settingEditors = document.querySelectorAll(".single-setting-editor");
    settingEditors.forEach(editor => {
        const settingPath = editor.dataset.setting_path;

        const valueInput = document.getElementById(`value-input-${settingPath}`);
        const editorContainer = document.getElementById(`editor-elements-${settingPath}`);

        if (!valueInput || !editorContainer) return; // safety check

        // Show/hide editor controls when input changes
        valueInput.addEventListener("input", () => {
            editorContainer.style.display = (valueInput.value !== valueInput.dataset.original) ? "flex" : "none";
        });

        // Reset button
        const resetBtn = editorContainer.querySelector(".button-reset");
        if (resetBtn) {
            resetBtn.addEventListener("click", () => {
                valueInput.value = valueInput.dataset.original;
                editorContainer.style.display = "none";
            });
        }

        // Save button
        const saveBtn = editorContainer.querySelector(".button-save");
        if (saveBtn) {
            saveBtn.addEventListener("click", async () => {
                await saveValue(settingPath, valueInput);
                editorContainer.style.display = "none";
                console.log("Saved:", valueInput.value);
            });
        }
    });
});

async function saveValue(settingPath, inputElement) {
    const payload = { current_value: inputElement.value };

    try {
        const response = await fetch(`/api/setting/${settingPath}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error(`Request failed: ${response.status}`);
        }

        const data = await response.json();
        inputElement.value = data.current_value ?? inputElement.dataset.original; // fallback if API doesn't return
        inputElement.dataset.original = data.current_value ?? inputElement.dataset.original
    } catch (err) {
        console.error("Error saving setting:", err);
    }
}
