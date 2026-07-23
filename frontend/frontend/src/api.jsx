  import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
  timeout: 30000,
});

export const registerUser = async (payload) => {
  const response = await API.post("/auth/register", payload);
  return response.data;
};

export const loginUser = async (payload) => {
  const response = await API.post("/auth/login", payload);
  return response.data;
};

export const uploadResume = async (file, jobTitle, jobDescription, token) => {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("job_title", jobTitle);
  formData.append("job_description", jobDescription);

  const response = await API.post("/resume/upload", formData, {
    headers: {
      Authorization: `Bearer ${token}`,
      // DO NOT manually set multipart boundary here
    },
  });

  return response.data;
};

export const getRecruiterResumes = async (token) => {
  const response = await API.get("/recruiter/resumes", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return response.data;
};

export default API;