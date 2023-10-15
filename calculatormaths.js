function getKnockback(percent, damagestaled, damageunstaled, weight, growth, base, setKnockback, crouch,
  grounded, trajectory, character) {

    var kb = null;

    if (setKnockback == 0)
        kb = ((0.01 * growth) * ((1.4 * (((0.05 * (damageunstaled * (damagestaled + Math.floor(percent)))) + (damagestaled + Math.floor(percent)) * 0.1) * (2.0 - (2.0 * (weight * 0.01)) / (1.0 + (weight * 0.01))))) + 18) + base);
    else
        kb = ((((setKnockback * 10 / 20) + 1) * 1.4 * (200 / (weight + 100)) + 18) * (growth / 100)) + base;

    if (crouch)
        kb *= 0.667;

    //cap knockback
    kb = Math.min(2500, kb);

    return kb;
}


// x and y are points on the control stick
function getAngle(traj, knockback, reverse)
{
    if (traj == 361)
    {
        //Sakurai Angle bullsheet
        if (knockback < 32.1 && grounded)
        {
          traj = 0;
          trajectory = 0;
        }
        else if (knockback >= 32.1 || !grounded)
        {
            traj = 44;
            trajectory = 44;
        }
    }

    //Angle offset is somewhere between -18 and 18 from DI
    var angleOffset = 0;
    var newtraj = traj - angleOffset;

    // if small or negative set to 0 ??
    if (newtraj < 0.01)
        newtraj = 0;

    return newtraj;
}

function getHorizontalVelocity(knockback, angle)
{
    var initialVelocity = knockback * 0.03;
    var horizontalAngle = Math.cos(angle * angleConversion);
    return initialVelocity * horizontalAngle;
}

function getVerticalVelocity(knockback, angle, grounded)
{
    var initialVelocity = knockback * 0.03;
    var verticalAngle = Math.sin(angle * angleConversion);
    //some hitting the ground bs is ignored
    return initialVelocity * verticalAngle;
}

function getHorizontalDecay(angle)
{
    var decay = 0.051 * Math.cos(angle * angleConversion)
    return decay;
}

function getVerticalDecay(angle)
{
    var decay = 0.051 * Math.sin(angle * angleConversion)
    return decay;
}


function Hit(percent, damagestaled, damageunstaled, growth, base, setKnockback, trajectory,
  character, version, xPos, yPos, crouch, reverse, tdiX, tdiY, fadeIn, doubleJump,
  sdix, sdiy, zdix, zdiy, adix, adiy, grounded, combo, comboFrame)
{

    var stayGrounded = false;
    var yDisplacement = 0;

    function knockbackTravel(horizontalVelocity, horizontalDecay, verticalVelocity, verticalDecay, character, hitstun, xPos, yPos, fadeIn, doubleJump, sdiVector, zdiVector, asdiVector, trajectory, meteorCancel, grounded, angle)
    {
        var positions = [];

        var hPos = xPos;
        var vPos = yPos;

        var horVelChar = 0;
        var verVelChar = 0;

        var horVelKB = horizontalVelocity;
        var verVelKB = verticalVelocity;

        var extendedDisplay = 0;

        var gravityFrames = Math.floor(characters[character]["terminalVelocity"] / characters[character]["gravity"]);
        var lastGravityFrame = characters[character]["terminalVelocity"] % characters[character]["gravity"];

        // for every frame of hitstun
        for (var i = 0; i < hitstun; i++)
        {

            //Knocked to the right
            if (horVelKB > 0)
            {
                //could try max(horVelKB-=horizontalDecay,0)
                horVelKB -= horizontalDecay;
                if (horVelKB < 0) horVelKB = 0;
            }
            //Knocked to the left
            else
            {
                horVelKB -= horizontalDecay;
                if (horVelKB > 0) horVelKB = 0;
            }

            //Knocked upwards
            if (verVelKB > 0)
            {
                verVelKB -= verticalDecay;
                if (verVelKB < 0) verVelKB = 0;
            }
            //Knocked downwards
            else
            {
                verVelKB -= verticalDecay;
                if (verVelKB > 0) verVelKB = 0;
            }


            if (i < gravityFrames) verVelChar -= characters[character]["gravity"];
            else if (i === gravityFrames) verVelChar -= lastGravityFrame;

            hPos = hPos + horVelChar + horVelKB;
            vPos = vPos + verVelChar + verVelKB;

            // Some SDI stuff ignored here

            positions.push([hPos, vPos, horVelKB, verVelKB, horVelChar, verVelChar]);
        }


        var hasDoubleJumped = false;
        var e = 0;

        //extendedDisplay is the amount of frames for the meteor cancel

        while (Math.abs(horVelKB) > 0.001 || Math.abs(verVelKB) > 0.001)
        {
            if (horVelKB != 0)
            {
                if (horVelKB > 0)
                {
                    horVelKB -= horizontalDecay;

                    if (horVelKB < 0)
                    {
                        horVelKB = 0;
                    }
                }
                else
                {
                    horVelKB -= horizontalDecay;
                    if (horVelKB > 0)
                    {
                        horVelKB = 0;
                    }
                }
            }

            if (verVelKB != 0)
            {
                if (verVelKB > 0)
                {
                    verVelKB -= verticalDecay;

                    if (verVelKB < 0)
                    {
                      verVelKB = 0;
                        verVelKB = 0;
                    }
                }
                else
                {
                    verVelKB -= verticalDecay;
                    if (verVelKB > 0)
                    {
                    }
                }
            }

            if (i < gravityFrames)
                verVelChar -= characters[character]["gravity"];
            else if (i == gravityFrames)
                verVelChar -= lastGravityFrame;

            if (doubleJump && !hasDoubleJumped)
            {
                if (characters[character]["djSetY"])
                {
                    verVelChar = characters[character]["djInitY"][e];

                    if (characters[character]["djSetX"])
                    {
                        if (hPos > 0) {
                            horVelChar += -characters[character]["djXValues"][e];
                        } else if (hPos < 0) {
                            horVelChar += characters[character]["djXValues"][e];
                        }
                    }

                    e++;

                }
                else
                {
                    verVelChar = characters[character]["djInitY"];

                    if (fadeIn)
                    {
                        if (hPos > 0)
                        {
                            horVelChar = -characters[character]["djInitX"];
                        }
                        else if (hPos < 0)
                        {
                            horVelChar = characters[character]["djInitX"];
                        }
                    }

                    hasDoubleJumped = true;
                }
            }

            if (hasDoubleJumped)
            {
                verVelChar -= characters[character]["gravity"];

                if (verVelChar < -characters[character]["terminalVelocity"])
                {
                    verVelChar = -characters[character]["terminalVelocity"];
                }
            }

            if (fadeIn)
            {
                if (hPos > 0)
                {
                    if (horVelChar < -characters[character]["driftMax"])
                    {
                        horVelChar += characters[character]["airFriction"];
                        if (horVelChar > -characters[character]["driftMax"])
                        {
                            horVelChar = -characters[character]["driftMax"];
                        }
                    }
                    else
                    {
                        horVelChar -= characters[character]["driftAcc"];
                        if (horVelChar < -characters[character]["driftMax"]) {
                            horVelChar = -characters[character]["driftMax"];
                        }
                    }
                }
                else if (hPos < 0)
                {
                    if (horVelChar > characters[character]["driftMax"])
                    {
                        horVelChar -= characters[character]["airFriction"];
                        if (horVelChar < characters[character]["driftMax"])
                        {
                            horVelChar = characters[character]["driftMax"];
                        }
                    }
                    else
                    {
                        horVelChar += characters[character]["driftAcc"];
                        if (horVelChar > characters[character]["driftMax"]) {
                            horVelChar = characters[character]["driftMax"];
                        }
                    }
                }
            }

            i++;
            hPos = hPos + horVelChar + horVelKB;
            vPos = vPos + verVelChar + verVelKB;
            positions.push([hPos, vPos, horVelKB, verVelKB, horVelChar, verVelChar]);
        }
        return positions;
    }



    function getHitstun(knockback)
    {
        return Math.floor(knockback * .4);
    }

    function getNewAngle(x, y)
    {
        var angle = Math.atan(Math.abs(y) / Math.abs(x));
        angle *= (180 / Math.PI);

        if (Math.sign(y) < 0)
        {
            if (Math.sign(x) > 0)
            {
                angle = 360 - angle;
            }
            else
            {
                angle += 180;
            }
        }
        else if (Math.sign(x) < 0)
        {
            angle = 180 - angle;
        }

        return angle;
    }

    function getNewKnockback(angle, horVel)
    {
        var horAngle = Math.cos(angle * angleConversion);
        var initVel = Math.abs(horVel / horAngle);
        return initVel / 0.03;
    }

    var angleConversion = Math.PI / 180;
    var weight = characters[character]["NTSCweight"];
    var gravity = characters[character]["gravity"];

    var releasePoint = [0, 0];
    var tFrames = [-1, -1];

    var knockback = getKnockback(percent, damagestaled, damageunstaled, weight, growth, base, setKnockback, crouch, chargeInterrupt, vcancel, grounded, trajectory, metal, ice, isThrow, character, yoshiDJArmor);
    var oldknockback = knockback;
    var hitstun = getHitstun(knockback);
    var horizontalVelocity;
    var verticalVelocity;

    var angle = getAngle(trajectory, knockback, reverse, tdiX, tdiY);
    horizontalVelocity = getHorizontalVelocity(knockback, angle, gravity);
    verticalVelocity = getVerticalVelocity(knockback, angle, grounded);
    angle = getNewAngle(horizontalVelocity, verticalVelocity);

    var horizontalDecay = getHorizontalDecay(angle);
    var verticalDecay = getVerticalDecay(angle);

    this.positions = knockbackTravel(horizontalVelocity, horizontalDecay, verticalVelocity, verticalDecay, character, hitstun, xPos, yPos, fadeIn, doubleJump, sdiVector, zdiVector, asdiVector, trajectory, meteorCancel, grounded, angle, releasePoint, icg, isThrow);
    this.hitstun = hitstun;

}
