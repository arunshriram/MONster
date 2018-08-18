// calculate acc.s0+value with error compensation
// see https://en.wikipedia.org/wiki/Kahan_summation_algorithm
// unless wikipedia, here the exact value = acc.s0 + acc.s1 (performed in higher precision)
static inline float2 kahan_sum(float2 acc, float value)
{
    if (value)
    {
        float sum = acc.s0;
        float err = acc.s1;
        if (fabs(value) > fabs(sum))
        {
            float tmp = sum;
            sum = value;
            value = tmp;
        }

        float cor = value + err;
        float target = sum + cor;
        err = cor - (target - sum);
        return (float2)(target, err);
    }
    else
    {
        return acc;
    }
}

// calculate a*b with error compensation
// see https://hal.archives-ouvertes.fr/hal-01367769/document
static inline float2 comp_prod(float a, float b)
{
    float x = a * b;
    float y = fma(a, b, -x);
    return (float2)(x, y);
}

// calculate a + b with error compensation
static inline float2 compensated_sum(float2 a, float2 b)
{
    float err = a.s1 + b.s1;
    float first = a.s0;
    float second = b.s0;
    if (fabs(second) > fabs(first))
    {
        float tmp = first;
        first = second;
        second = tmp;
    }
    float cor = second + err;
    float target = first + cor;
    err = cor - (target - first);
    return (float2)(target, err);
}

// calculate a * b with error compensation
static inline float2 compensated_mul(float2 a, float2 b)
{
    float2 tmp;
    tmp = kahan_sum((float2)(a.s0*b.s0, a.s0*b.s1), a.s1*b.s0);
    tmp = kahan_sum(tmp, a.s1*b.s1);
    return tmp;
}

// calculate a.b where a and b are float2
static inline float2 comp_dot2(float2 a, float2 b)
{
    return compensated_sum(comp_prod(a.s0, b.s0), comp_prod(a.s1, b.s1));
}

// calculate a.b where a and b are float3
static inline float2 comp_dot3(float3 a, float3 b)
{
    return compensated_sum(compensated_sum(comp_prod(a.s0, b.s0), comp_prod(a.s1, b.s1)), comp_prod(a.s2, b.s2));
}

// calculate a.b where a and b are float4
static inline float2 comp_dot4(float4 a, float4 b)
{
    return compensated_sum(compensated_sum(comp_prod(a.s0, b.s0), comp_prod(a.s1, b.s1)),
                           compensated_sum(comp_prod(a.s2, b.s2), comp_prod(a.s3, b.s3)));
}

// calculate a.b where a and b are float8
static inline float2 comp_dot8(float8 a, float8 b)
{
    return compensated_sum(
            compensated_sum(compensated_sum(comp_prod(a.s0, b.s0), comp_prod(a.s1, b.s1)),
                           compensated_sum(comp_prod(a.s2, b.s2), comp_prod(a.s3, b.s3))),
            compensated_sum(compensated_sum(comp_prod(a.s4, b.s4), comp_prod(a.s5, b.s5)),
                           compensated_sum(comp_prod(a.s6, b.s6), comp_prod(a.s7, b.s7))));
}

// calculate a.b where a and b are float8
static inline float2 comp_dot16(float16 a, float16 b)
{
    return compensated_sum(
             compensated_sum(
               compensated_sum(compensated_sum(comp_prod(a.s0, b.s0), comp_prod(a.s1, b.s1)),
                               compensated_sum(comp_prod(a.s2, b.s2), comp_prod(a.s3, b.s3))),
               compensated_sum(compensated_sum(comp_prod(a.s4, b.s4), comp_prod(a.s5, b.s5)),
                               compensated_sum(comp_prod(a.s6, b.s6), comp_prod(a.s7, b.s7)))),
             compensated_sum(
               compensated_sum(compensated_sum(comp_prod(a.s8, b.s8), comp_prod(a.s9, b.s9)),
                               compensated_sum(comp_prod(a.sa, b.sa), comp_prod(a.sb, b.sb))),
               compensated_sum(compensated_sum(comp_prod(a.sc, b.sc), comp_prod(a.sd, b.sd)),
                               compensated_sum(comp_prod(a.se, b.se), comp_prod(a.sf, b.sf)))));
}
