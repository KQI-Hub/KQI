![KQI Logo](KQI-Logo.svg) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ![KMI Logo](KMI-Logo.svg)
# KQ Image & KQI Model for Images (KMI)

# KQI
KQI is an image format developed by the KQI Hub. It uses the Haar Wavelet, YCoCg-R, 8-bit Companding for Chroma and Haar Coefficients, scQOI2, and Huffman coding.
It supports Lossy 24-bit RGB images with Lossless 8-bit Alpha.

KQI's bitstream is comprised of PNG-like chunks, with TwoCC IDs and uint48 sizes, allowing for chunks of up to 256TiB.
KQI supports embedding ICC profiles, as well as various types of metadata, such as time of creation, encoder data, license data, image description, and arbitrary text comments.
# KMI
KMI is the KQI Image Format's reference implementation, implemented in stlib Python 3. KMI aims to serve as a simple readable implementation for KQI that should also offer decent encoding performance and support all of baseline KQI's features.
