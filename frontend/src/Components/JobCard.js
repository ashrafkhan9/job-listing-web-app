import React from 'react';
import DeleteJob from './DeleteJob';

const JobCard = ({ job, onEdit, onDelete }) => {
  const formatDate = (dateString) => {
    try {
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
    } catch (error) {
      return 'Date not available';
    }
  };



  const renderTags = () => {
    if (!job.tags) return null;
    
    const tags = Array.isArray(job.tags) ? job.tags : job.tags.split(',');
    return tags.filter(tag => tag.trim()).map((tag, index) => (
      <span key={index} className="tag">
        {tag.trim()}
      </span>
    ));
  };

  return (
    <div className="job-card">
      <div className="job-header">
        <h3 className="job-title">{job.title}</h3>
        <div className="job-company">{job.company}</div>
        <div className="job-location">📍 {job.location}</div>
      </div>

      <div className="job-meta">
        <span className="job-type">{job.job_type || 'Full-time'}</span>
        <span className="job-date">
          Posted: {formatDate(job.posting_date)}
        </span>
      </div>

      {job.tags && (
        <div className="job-tags">
          {renderTags()}
        </div>
      )}

      {job.description && (
        <div className="job-description">
          {job.description}
        </div>
      )}

      <div className="job-actions">
        {job.url && (
          <a 
            href={job.url} 
            target="_blank" 
            rel="noopener noreferrer" 
            className="btn btn-view"
          >
            View Original
          </a>
        )}
        <button
          className="btn btn-edit"
          onClick={() => onEdit(job)}
        >
          Edit
        </button>
        <DeleteJob job={job} onDelete={onDelete} />
      </div>
    </div>
  );
};

export default JobCard;
