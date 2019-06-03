# Changelog

## [v1.0] - 2018-05-30
### Added
- Uid, name, created, bucket_name fields to files json
- Retrieve files from some buckets
- This changelog

### Changed
- Add blank=True to attachments field in model
- In url config you must set app_label and model_name instead model
- In staff url config you also set app_label and model_name
- Instead path in file url, now used uid
- Filter json keys before response. View only 'uid', 'name', 'size', 'content_type'

### Removed
- Removed file_info function from storage

[1.0.0]: https://github.com/pik-software/apiqa-storage/compare/v0.6...v1.0
