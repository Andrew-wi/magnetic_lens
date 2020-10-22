# ----------------------------------------------------------------------------
# Propagation
# ----------------------------------------------------------------------------
from dependencies import *
from helper import *
from vector_field import *

# initialize plotting variables
plotZ = [[] for _ in range(int(n))]
plotX = [[] for _ in range(int(n))]

# step through time
def propagate(p, v, a, successes, successful_particles, l_4k_to_lens_aperture, m_s):
    print('Propagating...')
    for index in range(0, int(n) * 3, 3):
        plotZ[int(index / 3)].append(p[index + 2])
        plotX[int(index / 3)].append(p[index])
    for time in np.linspace(0, t_final, num=steps, endpoint=False):
        for index in range(0, int(n)*3, 3):
            # 4k aperture
            if l_cell_to_4k <= p[index + 2] <= l_cell_to_4k + 0.01 and \
                ((p[index] ** 2 + p[index + 1] ** 2) ** (1/2)) > 0.003:
                v[index:index + 3] = 0
                a[index:index + 3] = 0
            # lens --------------
            elif l_cell_to_4k + l_4k_to_lens_aperture - 0.006 <= p[index + 2] \
                    <= l_cell_to_4k + l_4k_to_lens_aperture + 1.34 and\
                    ((p[index] ** 2 + p[index + 1] ** 2) ** (1/2)) < 0.003:
                # mesh spacing length
                l_xy = (r_inner*2/1e3)/(mxy-1)
                l_z = z_length/(mz-1)
                # coordinates for interpolation
                xCoord = round((r_inner/1e3 + p[index]) / l_xy)
                yCoord = round((r_inner/1e3 + p[index + 1]) / l_xy)
                zCoord = round((p[index + 2] - (l_cell_to_4k + l_4k_to_lens_aperture) - 0.006) / l_z)
                # todo: keep track of m_s, change sign of force field when \delta = 0
                delta_w_to_s = 2*np.pi*(-del_0_w_to_s + mu_B*g*m_s[int(index/3)]*np.absolute(normBMatrix[int(yCoord), int(xCoord), int(zCoord)])/h + v[index+2]/lambda_trans)
                delta_s_to_w = 2*np.pi*(del_0_s_to_w + mu_B*g*m_s[int(index/3)]*np.absolute(normBMatrix[int(yCoord), int(xCoord), int(zCoord)])/h + v[index+2]/lambda_trans)
                # breakpoint()
                if int(index/3)==31:
                    print([delta_w_to_s, delta_s_to_w, normBMatrix[int(yCoord), int(xCoord), int(zCoord)]])
                # flip sign accordingly
                if delta_w_to_s == 0:
                    m_s[int(index/3)] = 0.5
                    print('Flipped state to +')
                elif delta_s_to_w == 0:
                    m_s[int(index/3)] = -0.5
                    print('Flipped state to -')
                # change acceleration
                a[index:index + 3] = m_s[int(index/3)]*force_field[int(yCoord), int(xCoord), int(zCoord)]/mass
            # lens ---------------
            # # beam shutter
            # elif l_cell_to_4k + l_4k_to_beam_shutter <= p[index + 2] <= l_cell_to_4k + l_4k_to_beam_shutter + 0.01 and \
            #     ((p[index] ** 2 + p[index + 1] ** 2) ** (1/2)) > 0.003:
            #     v[index:index + 3] = 0
            #     a[index:index + 3] = 0
            else:
                a[index:index + 3] = 0
        timestep = t_final / steps
        v += a * timestep
        p += v * timestep
        for index in range(0, int(n) * 3, 3):
            if -mot_side_length / 2 <= p[index] <= mot_side_length / 2 and \
                -mot_side_length / 2 <= p[index + 1] <= mot_side_length / 2 and \
                mot_left_edge <= p[index + 2] <= mot_left_edge + mot_side_length and \
                int(index / 3) not in successful_particles:
                successful_particles.append(int(index / 3))
                successes += 1
            plotZ[int(index / 3)].append(p[index + 2])
            plotX[int(index / 3)].append(p[index])
    return p, v, a, successes, plotZ, plotX, successful_particles
