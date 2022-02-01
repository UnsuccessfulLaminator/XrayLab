#version 430

#define TOTAL_SAMPLES 65536
#define SAMPLES_PER_INVOC 64

layout(local_size_x = SAMPLES_PER_INVOC, local_size_y = 1, local_size_z = 1) in;
layout(std430, binding = 2) buffer samples {
    vec2 s[TOTAL_SAMPLES];
};

uniform sampler2D tex;

void main() {
    uint id = gl_GlobalInvocationID[0];
    uint start = id*SAMPLES_PER_INVOC;
    uint end = start+SAMPLES_PER_INVOC;
    
    for(uint i = start; i < end; i++) s[i].x = texture(tex, s[i]).r;
}
