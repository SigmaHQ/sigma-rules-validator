# validate-sigma-rules

This action is used to validate Sigma rules using the JSON schema. It is used to ensure that the rules are correctly formatted and that they will work with the Sigma converter.

## Usage

For an example repository structure, see the [example repository](https://github.com/mostafa/validate-sigma-rules-example).

```yaml
steps:
    - uses: mostafa/validate-sigma-rules@v0
      with:
        paths: './'
        schemaURL: 'https://raw.githubusercontent.com/SigmaHQ/sigma-specification/main/sigma-schema.json'
```

If you want to use an existing schema, you can use the `schemaFile` input:

```yaml
steps:
    - uses: mostafa/validate-sigma-rules@v0
      with:
        paths: './'
        schemaFile: './sigma-schema.json'
```

The `paths` can be used to provide multiple paths to the rules. For example, if you have a `rules` directory and a `custom-rules` directory, you can use the following:

```yaml
steps:
    - uses: mostafa/validate-sigma-rules@v0
      with:
        paths: |-
          ./rules
          ./custom-rules
```

## Inputs

### `paths` (optional)

The path(s) to the Sigma rules in your repository. This is a optional input and should be a relative path to the root of the repository. The default value is `./`.

### `schemaURL` (optional)

The URL to the latest version of the JSON schema for Sigma (or any other version or commit). This is an optional input and should be a URL to the JSON schema. The default value can be the latest version of the Sigma schema from the [sigma-specification repository](https://github.com/SigmaHQ/sigma-specification):

```yaml
...
schemaURL: 'https://raw.githubusercontent.com/SigmaHQ/sigma-specification/main/sigma-schema.json'
...
```

### `schemaFile` (optional)

The path to the JSON schema for Sigma. This is an optional input and should be a relative path to the root of the repository.

> [!IMPORTANT]
> Either `schemaURL` or `schemaFile` should be provided. If both are provided, an error will be thrown with a non-zero exit code. If `schemaFile` is provided and the file doesn't exist, an error will be thrown with a non-zero exit code. If none are provided, the action will use the default schema from the [sigma-specification repository](https://github.com/SigmaHQ/sigma-specification), as mentioned above.

## Outputs

It returns a zero exit code if the validation is successful and a non-zero exit code and errors if the validation fails.

## License

The scripts and documentation in this project are released under the [Apache-2.0 License](LICENSE).

## Contributions

Contributions are welcome! Just open an issue or a PR.
