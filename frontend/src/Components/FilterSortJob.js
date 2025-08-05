import React, { useState, useEffect } from 'react';

const FilterSort = ({ onFiltersChange, jobStats }) => {
  const [filters, setFilters] = useState({
    search: '',
    job_type: '',
    location: '',
    tag: '',
    sort: 'posting_date_desc'
  });

  const [availableLocations, setAvailableLocations] = useState([]);
  const [availableTags, setAvailableTags] = useState([]);

  useEffect(() => {
    // Extract unique locations and tags from job stats if available
    if (jobStats && jobStats.locations) {
      setAvailableLocations(jobStats.locations);
    }
    if (jobStats && jobStats.tags) {
      setAvailableTags(jobStats.tags);
    }
  }, [jobStats]);

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    const newFilters = {
      ...filters,
      [name]: value
    };
    setFilters(newFilters);
    onFiltersChange(newFilters);
  };

  const handleReset = () => {
    const resetFilters = {
      search: '',
      job_type: '',
      location: '',
      tag: '',
      sort: 'posting_date_desc'
    };
    setFilters(resetFilters);
    onFiltersChange(resetFilters);
  };

  const jobTypes = [
    'Full-time',
    'Part-time',
    'Contract',
    'Internship',
    'Temporary'
  ];

  const sortOptions = [
    { value: 'posting_date_desc', label: 'Date Posted: Newest First' },
    { value: 'posting_date_asc', label: 'Date Posted: Oldest First' },
    { value: 'title_asc', label: 'Job Title: A-Z' },
    { value: 'title_desc', label: 'Job Title: Z-A' },
    { value: 'company_asc', label: 'Company: A-Z' },
    { value: 'company_desc', label: 'Company: Z-A' }
  ];

  return (
    <div className="controls-section">
      <div className="controls-header">
        <h2 className="controls-title">Filter & Sort Jobs</h2>
        <div className="filter-actions">
          <button className="reset-btn" onClick={handleReset}>
            Reset Filters
          </button>
        </div>
      </div>

      <div className="filters">
        <div className="filter-group">
          <label htmlFor="search">Search</label>
          <input
            type="text"
            id="search"
            name="search"
            value={filters.search}
            onChange={handleFilterChange}
            placeholder="Search by title, company, or description..."
          />
        </div>

        <div className="filter-group">
          <label htmlFor="job_type">Job Type</label>
          <select
            id="job_type"
            name="job_type"
            value={filters.job_type}
            onChange={handleFilterChange}
          >
            <option value="">All Job Types</option>
            {jobTypes.map(type => (
              <option key={type} value={type}>{type}</option>
            ))}
          </select>
        </div>

        <div className="filter-group">
          <label htmlFor="location">Location</label>
          <input
            type="text"
            id="location"
            name="location"
            value={filters.location}
            onChange={handleFilterChange}
            placeholder="Filter by location..."
          />
        </div>

        <div className="filter-group">
          <label htmlFor="tag">Tags</label>
          <input
            type="text"
            id="tag"
            name="tag"
            value={filters.tag}
            onChange={handleFilterChange}
            placeholder="Filter by tag..."
          />
        </div>

        <div className="filter-group">
          <label htmlFor="sort">Sort By</label>
          <select
            id="sort"
            name="sort"
            value={filters.sort}
            onChange={handleFilterChange}
          >
            {sortOptions.map(option => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Active Filters Display */}
      {(filters.search || filters.job_type || filters.location || filters.tag) && (
        <div className="active-filters">
          <h4>Active Filters:</h4>
          <div className="filter-chips">
            {filters.search && (
              <span className="filter-chip">
                Search: "{filters.search}"
              </span>
            )}
            {filters.job_type && (
              <span className="filter-chip">
                Type: {filters.job_type}
              </span>
            )}
            {filters.location && (
              <span className="filter-chip">
                Location: {filters.location}
              </span>
            )}
            {filters.tag && (
              <span className="filter-chip">
                Tag: {filters.tag}
              </span>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default FilterSort;
