/**
 * Currency utilities for Indian Rupee (INR)
 */

export const formatINR = (amount: number): string => {
  if (amount >= 10000000) {
    // 1 Crore or more
    return `₹${(amount / 10000000).toFixed(2)} Cr`;
  } else if (amount >= 100000) {
    // 1 Lakh or more
    return `₹${(amount / 100000).toFixed(2)} L`;
  } else if (amount >= 1000) {
    // 1 Thousand or more
    return `₹${(amount / 1000).toFixed(2)} K`;
  } else {
    return `₹${amount.toFixed(2)}`;
  }
};

export const formatINRWithCommas = (amount: number): string => {
  return `₹${amount.toLocaleString('en-IN', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })}`;
};

export const CURRENCY_CONFIG = {
  symbol: '₹',
  code: 'INR',
  name: 'Indian Rupee',
  locale: 'en-IN',
};