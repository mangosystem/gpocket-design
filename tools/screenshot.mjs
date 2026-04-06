import puppeteer from 'puppeteer';

const browser = await puppeteer.launch({ headless: true, args: ['--no-sandbox'] });
const page = await browser.newPage();
// 캔버스 7800x5600 * 0.2 = 1560x1120 + 패딩
await page.setViewport({ width: 1700, height: 1500 });

await page.goto('file:///C:/Users/gurwl/kstar/project/gpocket-design/gpocket_renewal_v1.html', { waitUntil: 'networkidle0', timeout: 30000 });
await new Promise(r => setTimeout(r, 2000));

// zoomTo(0.2) 호출 + pan 조정
await page.evaluate(() => {
  window.zoomTo(0.2);
  // zoomTo가 panX=50,panY=20으로 설정하므로 추가 조정
  const canvas = document.getElementById('canvas');
  canvas.style.transform = `translate(20px, 20px) scale(0.2)`;
});

await new Promise(r => setTimeout(r, 1000));

// canvas-viewport 영역만 캡처
const el = await page.$('#canvas-viewport');
await el.screenshot({ path: 'preview.png' });

await browser.close();
console.log('done');
