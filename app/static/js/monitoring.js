import fetchData from './fetch.js';
import { startClock } from './clock.js';

fetchData();

const serverTimeString = document.getElementById('server-time').textContent.trim();
startClock(serverTimeString);
