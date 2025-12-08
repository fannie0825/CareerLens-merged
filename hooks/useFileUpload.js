import { useState } from 'react';
import ApiService from '../services/api';

/**
 * Custom hook for handling file uploads
 */
export const useFileUpload = (onSuccess, onError) => {
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [uploadedFile, setUploadedFile] = useState(null);

  const uploadFile = async (file) => {
    if (!file) {
      onError?.('Please select a file');
      return;
    }

    // Validate file type
    const validTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    const validExtensions = ['.pdf', '.docx'];
    const fileExtension = '.' + file.name.split('.').pop().toLowerCase();

    if (!validTypes.includes(file.type) && !validExtensions.includes(fileExtension)) {
      onError?.('Invalid file type. Please upload a PDF or DOCX file.');
      return;
    }

    // Validate file size (max 10MB)
    const maxSize = 10 * 1024 * 1024; // 10MB
    if (file.size > maxSize) {
      onError?.('File size exceeds 10MB limit.');
      return;
    }

    setUploading(true);
    setProgress(0);

    try {
      // Simulate progress for better UX
      const progressInterval = setInterval(() => {
        setProgress((prev) => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return 90;
          }
          return prev + 10;
        });
      }, 200);

      // Upload file
      const result = await ApiService.uploadResume(file);
      
      clearInterval(progressInterval);
      setProgress(100);
      setUploadedFile(result);

      // Extract profile after upload
      if (result.id) {
        try {
          const profile = await ApiService.extractProfile(result.id);
          onSuccess?.(result, profile);
        } catch (extractError) {
          console.error('Profile extraction error:', extractError);
          onSuccess?.(result, null); // Still succeed upload even if extraction fails
        }
      } else {
        onSuccess?.(result, null);
      }
    } catch (error) {
      console.error('Upload error:', error);
      onError?.(error.message || 'Upload failed. Please try again.');
    } finally {
      setUploading(false);
      setTimeout(() => setProgress(0), 1000);
    }
  };

  const reset = () => {
    setUploadedFile(null);
    setProgress(0);
    setUploading(false);
  };

  return {
    uploadFile,
    uploading,
    progress,
    uploadedFile,
    reset,
  };
};
