// ...existing code...

document.addEventListener('DOMContentLoaded', () => {
	const saveBtn = document.getElementById('saveTabs');
	const importBtn = document.getElementById('importTabs');
	const importFile = document.getElementById('importFile');
	const statusDiv = document.getElementById('status');

	saveBtn.addEventListener('click', async () => {
		statusDiv.textContent = '';
		chrome.windows.getAll({populate: true}, (windows) => {
			let lines = [];
			windows.forEach((win, idx) => {
				lines.push(`Window ${idx + 1}`);
				win.tabs.forEach(tab => {
					lines.push(`[${tab.title}, ${tab.url}]`);
				});
				lines.push(''); // empty line between windows
			});
			const now = new Date();
			const pad = n => n.toString().padStart(2, '0');
			const timestamp = `${now.getFullYear()}-${pad(now.getMonth()+1)}-${pad(now.getDate())}-${pad(now.getHours())}${pad(now.getMinutes())}${pad(now.getSeconds())}`;
			const filename = `TabulaSean-${timestamp}.txt`;
			const blob = new Blob([lines.join('\n')], {type: 'text/plain'});
			chrome.downloads.download({
				url: URL.createObjectURL(blob),
				filename,
				saveAs: true
			}, () => {
				statusDiv.textContent = 'Tabs from all windows saved!';
			});
		});
	});

	importBtn.addEventListener('click', () => {
		importFile.click();
	});

	importFile.addEventListener('change', (e) => {
		statusDiv.textContent = '';
		const file = e.target.files[0];
		if (!file) return;
		const reader = new FileReader();
		reader.onload = function(ev) {
			const lines = ev.target.result.split('\n');
			let opened = 0;
			lines.forEach(line => {
				const match = line.match(/^\[(.*?), (https?:\/\/[^\]]+)\]$/);
				if (match) {
					const url = match[2];
					chrome.tabs.create({url});
					opened++;
				}
			});
			statusDiv.textContent = `Opened ${opened} tabs.`;
		};
		reader.readAsText(file);
	});
});
