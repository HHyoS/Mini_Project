################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../ra/fsp/src/r_sci_i2c/r_sci_i2c.c 

C_DEPS += \
./ra/fsp/src/r_sci_i2c/r_sci_i2c.d 

OBJS += \
./ra/fsp/src/r_sci_i2c/r_sci_i2c.o 

SREC += \
bhc.srec 

MAP += \
bhc.map 


# Each subdirectory must supply rules for building sources it contributes
ra/fsp/src/r_sci_i2c/%.o: ../ra/fsp/src/r_sci_i2c/%.c
	$(file > $@.in,-mcpu=cortex-m33 -mthumb -mfloat-abi=hard -mfpu=fpv5-sp-d16 -O2 -fmessage-length=0 -fsigned-char -ffunction-sections -fdata-sections -Wunused -Wuninitialized -Wall -Wextra -Wmissing-declarations -Wconversion -Wpointer-arith -Wshadow -Wlogical-op -Waggregate-return -Wfloat-equal  -g -gdwarf-4 -D_RA_CORE=CM33 -D_RENESAS_RA_ -I"C:/Users/multicampus/e2_studio/workspace/bhc/src" -I"C:/Users/multicampus/e2_studio/workspace/bhc/ra/fsp/inc" -I"C:/Users/multicampus/e2_studio/workspace/bhc/ra/fsp/inc/api" -I"C:/Users/multicampus/e2_studio/workspace/bhc/ra/fsp/inc/instances" -I"C:/Users/multicampus/e2_studio/workspace/bhc/ra/arm/CMSIS_5/CMSIS/Core/Include" -I"C:/Users/multicampus/e2_studio/workspace/bhc/ra_gen" -I"C:/Users/multicampus/e2_studio/workspace/bhc/ra_cfg/fsp_cfg/bsp" -I"C:/Users/multicampus/e2_studio/workspace/bhc/ra_cfg/fsp_cfg" -std=c99 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" -c -o "$@" -x c "$<")
	@echo Building file: $< && arm-none-eabi-gcc @"$@.in"

