// mongoFrontend.js removed: use server-side proxy endpoints instead (/mongo/market, /mongo/news).
// This file is a safe stub to prevent accidental client-side DB usage.

function notSupported() {
  throw new Error('Direct client-side Mongo access is disabled. Use backend proxy endpoints (/mongo/market, /mongo/news).');
}

export function setMongoConfig() { notSupported(); }
export function getConfig() { notSupported(); }
export async function getMarketDocuments() { notSupported(); }
export async function getNewsDocuments() { notSupported(); }

export default {
  setMongoConfig,
  getConfig,
  getMarketDocuments,
  getNewsDocuments,
};
