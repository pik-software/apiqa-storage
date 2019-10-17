# Changelog

## [v2.5] - 2019-10-17
### Changed
- Add default ordering param for Attachment model
- Add search and filters at `AttachmentAdmin`
- Improve `AttachmentAdmin` performance

## [v2.4] - 2019-08-01
### Changed
- Increase max length on name field 

## [v2.3] - 2019-07-29
### Changed
- Bump minimal DRF version to 3.9

## [v2.2] - 2019-07-03
### Added
- Add task purge_attachments

## [v2.1] - 2019-07-01
### Added
- Add get param `uid` on upload file

## [v2.0] - 2019-06-17
### Added
- Model `Attachment` with generic relation, that stores all attachments data
- `AttachmentSerializerMixin` for serializers for models with attachments

### Removed
- `AttachFilesSerializers`, `CreateAttachFilesSerializers`

## [v1.1] - 2019-06-07
### Added
- In url config you can set **app_labels** instead a model or app_label, model_name.
  Ex: app_labels = ['project.Model', 'project.Model2']

### Changed
- Now in url config you can set only app_label without model_name. Ex: app_label='project.Model'

### Deprecated
- model argument in url config will be removed in v1.2

## [v1.0] - 2019-05-30
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

[v2.5]: https://github.com/pik-software/apiqa-storage/compare/v2.4...v2.5
[v2.4]: https://github.com/pik-software/apiqa-storage/compare/v2.3...v2.4
[v2.3]: https://github.com/pik-software/apiqa-storage/compare/v2.2...v2.3
[v2.2]: https://github.com/pik-software/apiqa-storage/compare/v2.1...v2.2
[v2.1]: https://github.com/pik-software/apiqa-storage/compare/v2.0...v2.1
[v2.0]: https://github.com/pik-software/apiqa-storage/compare/v1.1...v2.0
[v1.1]: https://github.com/pik-software/apiqa-storage/compare/v1.0...v1.1
[v1.0]: https://github.com/pik-software/apiqa-storage/compare/v0.6...v1.0
