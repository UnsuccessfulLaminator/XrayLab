#version 430

#define SAMPLES

layout(local_size_x = 1, local_size_y = 1, local_size_z = 1) in;
layout(std430, binding = 2) buffer samples {
    vec2 s[1024];
};

uniform sampler2D tex;

void main() {
    uint i = gl_GlobalInvocationID[0];

    s[i].x = texture(tex, s[i]).r;
    s[i].y = i;
}
