import axios, { AxiosRequestConfig } from "axios";

const axiosBaseParams: AxiosRequestConfig = {
  baseURL: process.env.VUE_APP_SEARCH_URI,
};

const axiosInstance = axios.create(axiosBaseParams);

const openErrorNotification = (message: string) => {
  // TODO: maybe render a toast here?
  alert(message);
};

axiosInstance.interceptors.response.use(
  (res) => res,
  (err) => {
    const status = err?.response?.status;

    if (status === 400 || status === 500) {
      const data = err.response.data;

      if (typeof data === "object" && data.message) {
        const text = `Es ist ein Fehler aufgetreten:
      
${data.message}`;

        console.error(text);
        openErrorNotification(text);
      } else if (typeof data === "string" && data.length !== 0) {
        const text = `Es ist ein Fehler aufgetreten:
      
${data}`;

        console.error(text);
        openErrorNotification(text);
      } else {
        openErrorNotification("Es ist ein Fehler aufgetreten");
      }
    }
    throw err;
  }
);

export default axiosInstance;
