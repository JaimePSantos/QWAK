$(function () {
    $('#testRunWalkBut').on('click', async function (e) {
        await setStaticProbDistDBTest();
    });
});

$(function () {
    $('#testGetRunWalkBut').on('click', async function (e) {
        await getStaticProbDistDBTest();
    });
});

$(function () {
    $('#resetBut').on('click', async function (e) {
        await reset();
    });
});

$(function () {
    $('#loadBut').on('click', async function (e) {
        await load();
    });
});

export async function setStaticProbDistDBTest() {
    await $.ajax({
        type: 'POST',
        url: `/setRunWalkDBTest`,
        success: function () {
            console.log(`success - Runwalk`);
        },
        error: function (response) {
            console.log('Runwalk error');
        }
    });
}

export async function getStaticProbDistDBTest() {
    await $.ajax({
        type: 'POST',
        url: `/getRunWalkDBTest`,
        success: function () {
            console.log(`success - Runwalk`);
        },
        error: function (response) {
            console.log('Runwalk error');
        }
    });
}

export async function reset() {
    await $.ajax({
        type: 'POST',
        url: `/reset`,
        success: function () {
            console.log(`success - reset`);
        },
        error: function (response) {
            console.log('Runwalk error');
        }
    });
}

export async function load() {
    await $.ajax({
        type: 'POST',
        url: `/load`,
        success: function () {
            console.log(`success - Walk loaded`);
        },
        error: function (response) {
            console.log('Runwalk error');
        }
    });
}