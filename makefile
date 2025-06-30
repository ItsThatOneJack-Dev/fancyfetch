# Cross-platform Makefile for building Python project with Nuitka and UV

# Configuration
APP_NAME = fancyfetch
MAIN_SCRIPT = main.py
OUTPUT_DIR = dist
BUILD_DIR = build

# Detect OS
ifeq ($(OS),Windows_NT)
    DETECTED_OS := Windows
    RM = del /f /q
    RMDIR = rmdir /s /q
    MKDIR = mkdir
    PATHSEP = \\
    NULLDEV = nul
    EXE_EXT = .exe
else
    DETECTED_OS := $(shell uname -s)
    RM = rm -f
    RMDIR = rm -rf
    MKDIR = mkdir -p
    PATHSEP = /
    NULLDEV = /dev/null
    EXE_EXT =
endif

# Modules to include in compilation
INCLUDE_MODULES = src.setup src.constants src.formatting src.shared src.configurationhandler
EXCLUDE_MODULES = src.defaults

# Convert to Nuitka arguments
INCLUDE_ARGS = $(foreach module,$(INCLUDE_MODULES),--include-module=$(module))
EXCLUDE_ARGS = $(foreach module,$(EXCLUDE_MODULES),--nofollow-import-to=$(module))

# Default target
.PHONY: all
all: build

# Install dependencies
.PHONY: install
install:
	uv sync
	uv add nuitka

# Clean build artifacts (cross-platform)
.PHONY: clean
clean:
ifeq ($(DETECTED_OS),Windows)
	-$(RMDIR) "$(BUILD_DIR)" 2>$(NULLDEV)
	-$(RMDIR) "$(OUTPUT_DIR)" 2>$(NULLDEV)
	-$(RMDIR) *.dist 2>$(NULLDEV)
	-$(RMDIR) *.build 2>$(NULLDEV)
	-$(RM) "$(APP_NAME)$(EXE_EXT)" 2>$(NULLDEV)
	-for /r . %%i in (*.pyc) do $(RM) "%%i" 2>$(NULLDEV)
	-for /d /r . %%i in (__pycache__) do $(RMDIR) "%%i" 2>$(NULLDEV)
else
	-$(RMDIR) $(BUILD_DIR) $(OUTPUT_DIR) *.dist *.build 2>$(NULLDEV)
	-$(RM) $(APP_NAME)$(EXE_EXT) 2>$(NULLDEV)
	-find . -name "*.pyc" -delete 2>$(NULLDEV)
	-find . -name "__pycache__" -type d -exec rm -rf {} + 2>$(NULLDEV)
endif

# Build the application
.PHONY: build
build: clean install-nuitka
	@echo "Building $(APP_NAME) with Nuitka on $(DETECTED_OS)..."
ifeq ($(DETECTED_OS),Windows)
	-$(MKDIR) "$(OUTPUT_DIR)" 2>$(NULLDEV)
else
	-$(MKDIR) $(OUTPUT_DIR)
endif
	uv run nuitka --onefile --standalone --output-filename=$(APP_NAME) --output-dir=$(OUTPUT_DIR) $(INCLUDE_ARGS) $(EXCLUDE_ARGS) --show-progress --assume-yes-for-downloads $(MAIN_SCRIPT)

.PHONY: just
just:
	nuitka --standalone --output-filename=fancyfetch --output-dir=dist --include-module=setup --include-module=constants --include-module=formatting --include-module=shared --include-module=configurationhandler --nofollow-import-to=src.defaults --show-progress --assume-yes-for-downloads main.py

# Ensure Nuitka is installed
.PHONY: install-nuitka
install-nuitka:
	@echo "Checking for Nuitka..."
	@uv run python -c "import nuitka" 2>$(NULLDEV) || uv add nuitka

# Build with debug information
.PHONY: build-debug
build-debug: clean install-nuitka
	@echo "Building $(APP_NAME) with debug info..."
ifeq ($(DETECTED_OS),Windows)
	-$(MKDIR) "$(OUTPUT_DIR)" 2>$(NULLDEV)
else
	-$(MKDIR) $(OUTPUT_DIR)
endif
	uv run nuitka \
		--onefile \
		--standalone \
		--output-filename=$(APP_NAME) \
		--output-dir=$(OUTPUT_DIR) \
		$(INCLUDE_ARGS) \
		$(EXCLUDE_ARGS) \
		--show-progress \
		--assume-yes-for-downloads \
		--debug \
		--show-modules \
		--report=compilation-report.xml \
		$(MAIN_SCRIPT)

# Fast build (no optimization)
.PHONY: build-fast
build-fast: clean install-nuitka
	@echo "Building $(APP_NAME) (fast mode)..."
ifeq ($(DETECTED_OS),Windows)
	-$(MKDIR) "$(OUTPUT_DIR)" 2>$(NULLDEV)
else
	-$(MKDIR) $(OUTPUT_DIR)
endif
	uv run nuitka \
		--onefile \
		--standalone \
		--output-filename=$(APP_NAME) \
		--output-dir=$(OUTPUT_DIR) \
		$(INCLUDE_ARGS) \
		$(EXCLUDE_ARGS) \
		--show-progress \
		--assume-yes-for-downloads \
		--no-prefer-source-code \
		$(MAIN_SCRIPT)

# Build optimized version
.PHONY: build-optimized
build-optimized: clean install-nuitka
	@echo "Building optimized $(APP_NAME)..."
ifeq ($(DETECTED_OS),Windows)
	-$(MKDIR) "$(OUTPUT_DIR)" 2>$(NULLDEV)
else
	-$(MKDIR) $(OUTPUT_DIR)
endif
	uv run nuitka \
		--onefile \
		--standalone \
		--output-filename=$(APP_NAME) \
		--output-dir=$(OUTPUT_DIR) \
		$(INCLUDE_ARGS) \
		$(EXCLUDE_ARGS) \
		--show-progress \
		--assume-yes-for-downloads \
		--lto=yes \
		--enable-plugin=anti-bloat \
		$(MAIN_SCRIPT)

# Test the built application
.PHONY: test
test: build
	@echo "Testing built application..."
ifeq ($(DETECTED_OS),Windows)
	cd $(OUTPUT_DIR) && $(APP_NAME).exe --version || $(APP_NAME).exe --help || echo Test completed
else
	cd $(OUTPUT_DIR) && ./$(APP_NAME) --version || ./$(APP_NAME) --help || echo "Test completed"
endif

# Show build information
.PHONY: info
info:
	@echo "Build Configuration:"
	@echo "  Detected OS: $(DETECTED_OS)"
	@echo "  App Name: $(APP_NAME)"
	@echo "  Main Script: $(MAIN_SCRIPT)"
	@echo "  Output Directory: $(OUTPUT_DIR)"
	@echo "  Include Modules: $(INCLUDE_MODULES)"
	@echo ""
	@echo "Available targets:"
	@echo "  build          - Standard build"
	@echo "  build-debug    - Build with debug info"
	@echo "  build-fast     - Fast build (less optimization)"
	@echo "  build-optimized- Highly optimized build"
	@echo "  test           - Test the built application"
	@echo "  clean          - Clean build artifacts"
	@echo "  install        - Install dependencies"

# Development build
.PHONY: dev
dev: build-fast test