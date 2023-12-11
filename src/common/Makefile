#build-<CloudFormationResourceName>
directory_name = "common"

build-CommonLibraryLayer:
	
	@echo "directory = ${directory_name}"
	mkdir "$(ARTIFACTS_DIR)/python"
	mkdir -p "$(ARTIFACTS_DIR)/python/${directory_name}"
	cp -R . "$(ARTIFACTS_DIR)/python/${directory_name}/"
	python3 -m pip install -r requirements.txt -t "$(ARTIFACTS_DIR)/python"

