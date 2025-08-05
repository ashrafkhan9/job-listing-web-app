import React, { useState, useEffect } from 'react';
import './App.css';
import { jobAPI } from './api.jsx';
import JobCard from './Components/JobCard';
import JobForm from './Components/AddEditJob';
import FilterSort from './Components/FilterSortJob';

function App() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [showJobForm, setShowJobForm] = useState(false);
  const [editingJob, setEditingJob] = useState(null);
  const [filters, setFilters] = useState({});
  const [jobStats, setJobStats] = useState(null);

  // Fetch jobs on component mount and when filters change
  useEffect(() => {
    fetchJobs();
  }, [filters]);

  // Fetch job statistics
  useEffect(() => {
    fetchJobStats();
  }, []);

  const fetchJobs = async () => {
    try {
      setLoading(true);
      setError('');
      const response = await jobAPI.getJobs(filters);
      setJobs(response.data || []);
    } catch (err) {
      setError(err.message || 'Failed to fetch jobs');
      console.error('Error fetching jobs:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchJobStats = async () => {
    try {
      const response = await jobAPI.getJobStats();
      setJobStats(response.data);
    } catch (err) {
      console.error('Error fetching job stats:', err);
    }
  };

  const handleAddJob = () => {
    setEditingJob(null);
    setShowJobForm(true);
  };

  const handleEditJob = (job) => {
    setEditingJob(job);
    setShowJobForm(true);
  };

  const handleDeleteJob = async (jobId) => {
    try {
      setError('');
      await jobAPI.deleteJob(jobId);
      setSuccess('Job deleted successfully!');
      fetchJobs(); // Refresh the job list
      fetchJobStats(); // Refresh stats
      
      // Clear success message after 3 seconds
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      setError(err.message || 'Failed to delete job');
    }
  };

  const handleJobSubmit = async (jobData) => {
    try {
      setError('');
      
      if (editingJob) {
        // Update existing job
        await jobAPI.updateJob(editingJob.id, jobData);
        setSuccess('Job updated successfully!');
      } else {
        // Create new job
        await jobAPI.createJob(jobData);
        setSuccess('Job added successfully!');
      }
      
      setShowJobForm(false);
      setEditingJob(null);
      fetchJobs(); // Refresh the job list
      fetchJobStats(); // Refresh stats
      
      // Clear success message after 3 seconds
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      setError(err.message || 'Failed to save job');
    }
  };

  const handleFormCancel = () => {
    setShowJobForm(false);
    setEditingJob(null);
  };

  const handleFiltersChange = (newFilters) => {
    setFilters(newFilters);
  };

  const clearMessages = () => {
    setError('');
    setSuccess('');
  };

  return (
    <div className="App">
      <header className="header">
        <div className="container">
          <h1>Job Listing Portal</h1>
          <p>Find your next actuarial opportunity</p>
        </div>
      </header>

      <main className="main-content">
        <div className="container">
          {/* Error and Success Messages */}
          {error && (
            <div className="error">
              {error}
              <button 
                style={{ float: 'right', background: 'none', border: 'none', cursor: 'pointer' }}
                onClick={clearMessages}
              >
                ×
              </button>
            </div>
          )}
          
          {success && (
            <div className="success">
              {success}
              <button 
                style={{ float: 'right', background: 'none', border: 'none', cursor: 'pointer' }}
                onClick={clearMessages}
              >
                ×
              </button>
            </div>
          )}

          {/* Controls Section */}
          <div className="controls-section">
            <div className="controls-header">
              <h2 className="controls-title">Job Management</h2>
              <button className="add-job-btn" onClick={handleAddJob}>
                + Add New Job
              </button>
            </div>

            {/* Job Statistics */}
            {jobStats && (
              <div className="job-stats">
                <div className="job-count">
                  Total Jobs: {jobStats.total_jobs || 0}
                </div>
                {jobStats.job_types && (
                  <div className="job-types-stats">
                    {Object.entries(jobStats.job_types).map(([type, count]) => (
                      <span key={type} className="job-type-stat">
                        {type}: {count}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Filter and Sort Controls */}
          <FilterSort 
            onFiltersChange={handleFiltersChange}
            jobStats={jobStats}
          />

          {/* Job Results */}
          <div className="job-stats">
            <div className="job-count">
              Showing {jobs.length} job{jobs.length !== 1 ? 's' : ''}
            </div>
          </div>

          {/* Loading State */}
          {loading && (
            <div className="loading">
              Loading jobs...
            </div>
          )}

          {/* Jobs Grid */}
          {!loading && jobs.length > 0 && (
            <div className="jobs-grid">
              {jobs.map(job => (
                <JobCard
                  key={job.id}
                  job={job}
                  onEdit={handleEditJob}
                  onDelete={handleDeleteJob}
                />
              ))}
            </div>
          )}

          {/* No Jobs State */}
          {!loading && jobs.length === 0 && (
            <div className="no-jobs">
              <h3>No jobs found</h3>
              <p>Try adjusting your filters or add a new job to get started.</p>
            </div>
          )}
        </div>
      </main>

      {/* Job Form Modal */}
      {showJobForm && (
        <JobForm
          job={editingJob}
          onSubmit={handleJobSubmit}
          onCancel={handleFormCancel}
          isEditing={!!editingJob}
        />
      )}
    </div>
  );
}

export default App;
