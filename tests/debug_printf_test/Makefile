TARGET_EXEC ?= test.xe
PROJ_ROOT = ../..
BUILD_DIR ?= ./build/very/deep


#list the source files we care about
SRCS := ./src/main.xc

#Add dep lib sources
SRCS += $(shell find ../../lib_logging -name '*.c')

OBJS := $(SRCS:%=$(BUILD_DIR)/%.o)
OBJS_FILE := $(notdir $(SRCS:%=$(BUILD_DIR)/%.o))

DEPS := $(OBJS:.o=.d)

INC_DIRS := $(shell find $(SRCS) -type d)
INC_DIRS += $(shell find $(PROJ_ROOT) -name api -type d)
INC_DIRS += $(dir $(SRCS))
INC_FLAGS := $(addprefix -I,$(INC_DIRS))

TARGET_FLAG ?= -target=XCORE-AI-EXPLORER
XCC ?= xcc

COMMON_FLAGS ?= $(INC_FLAGS) $(TARGET_FLAG) -Os -g -DDEBUG_PRINT_ENABLE=1
CFLAGS ?= -c 

XCFLAGS ?= -c
ASMFLAGS ?= $(INC_FLAGS) $(TARGET_FLAG)

$(TARGET_EXEC): $(OBJS) 
	$(XCC) $(TARGET_FLAG) -o $@ $^ -report

# c source
$(BUILD_DIR)/%.c.o: %.c
	$(MKDIR_P) $(dir $@)
	$(XCC) $(COMMON_FLAGS) $(CFLAGS) -c $< -o $@

# xc source
$(BUILD_DIR)/%.xc.o: %.xc
	$(MKDIR_P) $(dir $@)
	$(XCC) $(COMMON_FLAGS) $(XCFLAGS) -c $< -o $@

# asm source
$(BUILD_DIR)/%.S.o: %.S
	$(MKDIR_P) $(dir $@)
	$(XCC) $(ASMFLAGS) -c $< -o $@

.PHONY: clean

clean:
	$(RM) -r $(BUILD_DIR) build $(TARGET_EXEC)

-include $(DEPS)

MKDIR_P ?= mkdir -p