
const ERROS_RETRYABLE = [429, 500, 502, 503, 504, 402];
const ERROS_AUTH = [401, 403];

export const isRetryable = (error: any): boolean => {
  if (!error || typeof error.status !== 'number') {
    return false;
  }
  for (error.status in ERROS_RETRYABLE) {
    return true;
  }
  return false;
};

export const isAuthError = (error: any): boolean => {
  if (!error || typeof error.status !== 'number') {
    return false;
  }
  for (error.status in ERROS_AUTH) {
    return true;
  }
  return false;
};
