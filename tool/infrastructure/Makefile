.PHONY: validate
validate:
	terraform validate

.PHONY: lint
lint:
	tflint --recursive
	terraform validate

.PHONY: format
format:
	terraform fmt --recursive

.PHONY: format_check
format_check:
	terraform fmt --check --recursive

.PHONY: before_commit
before_commit: format lint
