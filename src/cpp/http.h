#ifdef _WIN32
extern int __cdecl
#else
extern int
#endif
httpGet(char const *URL, char const *page, unsigned int port, char **dataPtr);
