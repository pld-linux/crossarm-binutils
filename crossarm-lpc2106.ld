MEMORY
{
	FLASH(rx)	: ORIGIN = 0x00000000, LENGTH = 120K
	RAM(rw)		: ORIGIN = 0x40000000, LENGTH = 64K
}

__STACK_START__			= 0x40000000 + 64K;

__UNDEFINED_STACK_SIZE__	= 0x0004;
__ABORT_STACK_SIZE__		= 0x0004;
__SUPERVISOR_STACK_SIZE__	= 0x0200;
__FIQ_STACK_SIZE__		= 0x0080;
__IRQ_STACK_SIZE__		= 0x0080;

__UNDEFINED_SP__		= __STACK_START__ - 4;
__ABORT_SP__			= __UNDEFINED_SP__ - __UNDEFINED_STACK_SIZE__;
__SUPERVISOR_SP__		= __ABORT_SP__ - __ABORT_STACK_SIZE__;
__FIQ_SP__			= __SUPERVISOR_SP__ - __SUPERVISOR_STACK_SIZE__;
__IRQ_SP__			= __FIQ_SP__ - __FIQ_STACK_SIZE__;
__USER_SP__			= __IRQ_SP__ - __IRQ_STACK_SIZE__;

SECTIONS
{
	. = 0;
	.text :
	{
		__text_start__ = .;
		lpc210x-crt0.o(.text)
		*(.text)
		*(.glue_7)
		*(.glue_7t)
	}
	>FLASH =0xFF
	. = ALIGN(4);
	.rodata :
	{
		*(.rodata)
		*(.rodata*)
	}
	>FLASH =0xFF
	. = ALIGN(4);
	__text_end__ = .;

	.data : AT(__text_end__)
	{
		__data_start__ = .;
		*(.data)
	}
	>RAM
	. = ALIGN(4);
	__data_end__ = .;

	.bss :
	{
		__bss_start__ = .;
		*(.bss)
		*(COMMON)
	}
	>RAM
	. = ALIGN(4);
	__bss_end__ = .;
	_end = .;
	PROVIDE (end = .);
}

PROVIDE(undefined_instruction_handler	= endless_loop);
PROVIDE(software_interrupt_handler	= endless_loop);
PROVIDE(prefetch_abort_handler		= endless_loop);
PROVIDE(data_abort_handler		= endless_loop);
PROVIDE(irq_handler			= endless_loop);
PROVIDE(fiq_handler			= endless_loop);
