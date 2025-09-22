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
				let windowGroups = [];
				let currentGroup = [];
				lines.forEach(line => {
					if (/^Window \d+/.test(line)) {
						if (currentGroup.length > 0) {
							windowGroups.push(currentGroup);
							currentGroup = [];
						}
					} else if (/^\[.*?, https?:\/\/[^\]]+\]$/.test(line)) {
						const match = line.match(/^\[(.*?), (https?:\/\/[^\]]+)\]$/);
						if (match) {
							currentGroup.push(match[2]);
						}
					} else if (line.trim() === '') {
						if (currentGroup.length > 0) {
							windowGroups.push(currentGroup);
							currentGroup = [];
						}
					}
				});
				if (currentGroup.length > 0) {
					windowGroups.push(currentGroup);
				}
				let opened = 0;
				let createdWindows = 0;
				function openNextWindow(idx) {
					if (idx >= windowGroups.length) {
						statusDiv.textContent = `Opened ${opened} tabs in ${createdWindows} windows.`;
						return;
					}
					const urls = windowGroups[idx];
					if (urls.length === 0) {
						openNextWindow(idx + 1);
						return;
					}
					chrome.windows.create({url: urls[0]}, (win) => {
						createdWindows++;
						opened++;
						// Open remaining tabs in this window
						let tabsToOpen = urls.length - 1;
						if (tabsToOpen === 0) {
							openNextWindow(idx + 1);
							return;
						}
						let tabsOpened = 0;
						for (let i = 1; i < urls.length; i++) {
							chrome.tabs.create({windowId: win.id, url: urls[i]}, () => {
								opened++;
								tabsOpened++;
								if (tabsOpened === tabsToOpen) {
									openNextWindow(idx + 1);
								}
							});
						}
					});
				}
				openNextWindow(0);
			};
			reader.readAsText(file);
		});
});
