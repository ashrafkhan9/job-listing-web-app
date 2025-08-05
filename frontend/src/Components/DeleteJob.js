import React from 'react';

const DeleteJob = ({ job, onDelete }) => {
  const handleDelete = () => {
    if (window.confirm(`Are you sure you want to delete the job "${job.title}" at ${job.company}?`)) {
      onDelete(job.id);
    }
  };

  return (
    <button 
      className="btn btn-delete" 
      onClick={handleDelete}
      title={`Delete ${job.title}`}
    >
      Delete
    </button>
  );
};

export default DeleteJob;
