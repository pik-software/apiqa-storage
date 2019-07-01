# Changelog

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

[v2.1]: https://github.com/pik-software/apiqa-storage/compare/v2.0...v2.1
[v2.0]: https://github.com/pik-software/apiqa-storage/compare/v1.1...v2.0
[v1.1]: https://github.com/pik-software/apiqa-storage/compare/v1.0...v1.1
[v1.0]: https://github.com/pik-software/apiqa-storage/compare/v0.6...v1.0
