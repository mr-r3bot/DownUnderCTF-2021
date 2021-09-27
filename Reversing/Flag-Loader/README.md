### Flag Loader

There are 3 checks we need to pass:

check1
```
char check1(void)

{
  long in_FS_OFFSET;
  char null_byte;
  char local_1d;
  int i;
  byte 5_letters_buffer [6];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  null_byte = '\0';
  local_1d = '\x01';
  printf("Give me five letters: ");
  read(0,5_letters_buffer,5);
  for (i = 0; i < 5; i = i + 1) {
    null_byte = null_byte + (5_letters_buffer[i] ^ (&DUCTF_str)[i]);
    local_1d = local_1d * 5_letters_buffer[i] * ((char)i + '\x01');
  }
  if ((null_byte != '\0') || (local_1d == '\0')) {
    die();
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return local_1d;
}
```

We need to solve the XOR equation
