# validate-sigma-rules

This action is used to validate Sigma rules using the JSON schema. It is used to ensure that the rules are correctly formatted and that they will work with the Sigma converter.

## Usage

The simplest way to use the action is to use it without any inputs. This will use the default schema from the sigma-specification repository and validate the rules in the root of the repository.

```yaml
steps:
    - uses: SigmaHQ/validate-sigma-rules@v0
```

If you want to use a specific schema, you can use the `schemaURL` input. This will download the schema from the URL and use it for validation.

```yaml
steps:
    - uses: SigmaHQ/validate-sigma-rules@v0
      with:
        paths: './'
        schemaURL: 'https://raw.githubusercontent.com/SigmaHQ/sigma-specification/main/sigma-schema.json'
```

If you want to use an existing schema, you can use the `schemaFile` input. Note that the file must exist in the repository.

```yaml
steps:
    - uses: SigmaHQ/validate-sigma-rules@v0
      with:
        paths: './'
        schemaFile: './sigma-schema.json'
```

The `paths` can be used to provide multiple paths to the rules. For example, if you have a `rules` directory and a `custom-rules` directory, you can use the following syntax to provide both paths to the action:

```yaml
steps:
    - uses: SigmaHQ/validate-sigma-rules@v0
      with:
        paths: |-
          ./rules
          ./custom-rules
```

For an example of how to use the action, see the [Sigma repository](https://github.com/SigmaHQ/sigma/blob/master/.github/workflows/sigma-validation.yml).

## Inputs

The action has three inputs:

- `paths`: the path to the Sigma rules in the repository
- `schemaURL`: the URL to the JSON schema for Sigma
- `schemaFile`: the path to the JSON schema for Sigma

All of the inputs are optional. If the `schemaURL` is not provided, the action will use the default schema from the [sigma-specification repository](https://raw.githubusercontent.com/SigmaHQ/sigma-specification/main/sigma-schema.json). If the `schemaFile` is not provided, the action will use the `schemaURL` to download the file locally and use it for validation.

### `paths` (optional)

The path(s) to the Sigma rules in your repository. This is a optional input and should be a relative path to the root of the repository. The default value is `./`. It can be a single path or multiple paths separated by a newline.

```yaml
steps:
    - uses: SigmaHQ/validate-sigma-rules@v0
      with:
        paths: |-
          ./rules
          ./custom-rules
```

### `schemaURL` (optional)

The URL to the latest version of the JSON schema for Sigma (or any other version or commit). This is an optional input and should be a URL to the JSON schema. The default value is the latest version of the Sigma schema from the [sigma-specification repository](https://raw.githubusercontent.com/SigmaHQ/sigma-specification/main/sigma-schema.json):

```yaml
steps:
    - uses: SigmaHQ/validate-sigma-rules@v0
      with:
        schemaURL: 'https://raw.githubusercontent.com/SigmaHQ/sigma-specification/main/sigma-schema.json'
```

### `schemaFile` (optional)

The path to the JSON schema for Sigma. This is an optional input and should be a relative path to the root of the repository. Note that the file must exist in the repository. Both the `schemaURL` or the `schemaFile` can be provided, but the `schemaFile` will be used and if the file doesn't exist, it will be downloaded. If none are provided, the action will use the default schema from the [sigma-specification repository](https://raw.githubusercontent.com/SigmaHQ/sigma-specification/main/sigma-schema.json).

```yaml
steps:
    - uses: SigmaHQ/validate-sigma-rules@v0
      with:
        schemaFile: './sigma-schema.json'
```

## Outputs

It returns a zero exit code if the validation is successful and a non-zero exit code and errors if the validation fails.

## License

The scripts and documentation in this project are released under the [Apache-2.0 License](LICENSE).

## Contributions

Contributions are welcome! Just open an issue or a PR.
